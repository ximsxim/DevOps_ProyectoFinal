import boto3
import time

def main():
    print("--- Iniciando automatizacion con Boto3 ---\n")
    ec2 = boto3.client('ec2', region_name='us-east-1')
    s3 = boto3.client('s3')

    try:
        keys = ec2.describe_key_pairs(KeyNames=['llaves-devops'])
        if not keys['KeyPairs']:
            print("[ERROR] La llave 'llaves-devops' no existe en EC2. Crearla antes de ejecutar.")
            return
    except ec2.exceptions.ClientError as e:
        print(f"[ERROR] No se pudo verificar la llave: {e}")
        return

    try:
        instances = ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending']}]
        )
        running_count = sum(len(r['Instances']) for r in instances['Reservations'])
        if running_count >= 5:
            print("[ERROR] Limite de 5 instancias activas alcanzado. No se puede crear otra.")
            return
        print(f"Instancias activas actuales: {running_count}/5")
    except Exception as e:
        print(f"[ERROR] Al verificar limite: {e}")
        return

    print("1. Aprovisionando nueva instancia EC2...")
    try:
        nueva_instancia = ec2.run_instances(
            ImageId='ami-080e1f13689e07408',
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            KeyName='llaves-devops',
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'Instancia-Auto-Python'}]
            }]
        )
        instance_id = nueva_instancia['Instances'][0]['InstanceId']
        print(f"[EXITO] Instancia creada con ID: {instance_id}")
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        print(f"   La instancia {instance_id} esta en ejecucion.")
    except Exception as e:
        print(f"[ERROR] No se pudo crear la instancia: {e}")

    print("\n2. Reporte de Uso de Recursos (Instancias EC2):")
    try:
        reporte = ec2.describe_instances()
        for reserva in reporte['Reservations']:
            for inst in reserva['Instances']:
                id_inst = inst['InstanceId']
                tipo = inst['InstanceType']
                estado = inst['State']['Name']
                nombre = next((tag['Value'] for tag in inst.get('Tags', []) if tag['Key'] == 'Name'), 'Sin nombre')
                print(f"   - ID: {id_inst} | Nombre: {nombre} | Tipo: {tipo} | Estado: {estado}")
    except Exception as e:
        print(f"[ERROR] Al generar reporte: {e}")

    print("\n3. Listando Buckets S3 y sus objetos:")
    try:
        buckets = s3.list_buckets()
        if not buckets['Buckets']:
            print("   No se encontraron buckets en esta cuenta.")
        else:
            for bucket in buckets['Buckets']:
                nombre_bucket = bucket['Name']
                print(f"   * Bucket: {nombre_bucket}")
                try:
                    objetos = s3.list_objects_v2(Bucket=nombre_bucket)
                    if 'Contents' in objetos:
                        for obj in objetos['Contents']:
                            print(f"     -> Objeto: {obj['Key']} (Tamano: {obj['Size']} bytes)")
                    else:
                        print("     -> (El bucket esta vacio)")
                except Exception as e:
                    print(f"     [ERROR] No se pudo listar objetos: {e}")
    except Exception as e:
        print(f"[ERROR] Al listar S3: {e}")

if __name__ == '__main__':
    main()