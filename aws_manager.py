import boto3

def main():
    print("--- Iniciando automatización con Boto3 ---\n")
    ec2 = boto3.client('ec2', region_name='us-east-1')
    s3 = boto3.client('s3')

    print("1. Aprovisionando nueva instancia EC2 (respetando limites)...")
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
        print(f"   [ÉXITO] Instancia creada con ID: {instance_id}\n")
    except Exception as e:
        print(f"   [ERROR] No se pudo crear la instancia: {e}\n")

    print("2. Reporte de Uso de Recursos (Instancias EC2):")
    try:
        reporte = ec2.describe_instances()
        for reserva in reporte['Reservations']:
            for inst in reserva['Instances']:
                id_inst = inst['InstanceId']
                tipo = inst['InstanceType']
                estado = inst['State']['Name']
                print(f"   - ID: {id_inst} | Tipo: {tipo} | Estado: {estado}")
        print()
    except Exception as e:
        print(f"   [ERROR] Al generar reporte: {e}\n")

    print("3. Listando Buckets S3 y sus objetos:")
    try:
        buckets = s3.list_buckets()
        if not buckets['Buckets']:
            print("   No se encontraron buckets en esta cuenta.")
        else:
            for bucket in buckets['Buckets']:
                nombre_bucket = bucket['Name']
                print(f"   * Bucket: {nombre_bucket}")
                objetos = s3.list_objects_v2(Bucket=nombre_bucket)
                if 'Contents' in objetos:
                    for obj in objetos['Contents']:
                        print(f"     -> Objeto: {obj['Key']} (Tamaño: {obj['Size']} bytes)")
                else:
                    print("     -> (El bucket está vacío)")
    except Exception as e:
        print(f"   [ERROR] Al listar S3: {e}\n")

if __name__ == '__main__':
    main()