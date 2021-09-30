import boto3
import config

class TestLog(object):
    result = 'Test started'

    def Add(self, test_name, result, message = ''):
        self.result += f'\n-- {test_name}:'
        self.result += result
        if message == '':
            pass
        else:
            self.result += f'\n Message: {message}:'

    def Show(self):
        print(self.result)


def run():
    test_log = TestLog()

    # connection
    test_name = 'Connection to instance'    
    try:
        s3 = boto3.resource(
            service_name = 's3',
            region_name = config.region_name,
            aws_access_key_id = config.key.access,
            aws_secret_access_key = config.key.secret
        )
    except Exception as error:
        test_log.Add(test_name, 'FAILED', str(error))
    else:
        test_log.Add(test_name, 'DONE')

    # get bucket
    test_name = 'Connection to bucket'    
    try:
        bucket = s3.Bucket(config.s3_bucket)
    except Exception as error:
        test_log.Add(test_name, 'FAILED', str(error))
    else:
        test_log.Add(test_name, 'DONE')

    # listing objects
    test_name = 'Listing objects permission:'    
    try:
        objects = bucket.objects.all()
    except Exception as error:
        test_log.Add(test_name, 'FAILED', str(error))
    else:
        test_log.Add(test_name, 'GRANTED')

    # save objects
    test_name = 'Saving objects permission:'
    try:
        key_name = 'Hello'
        file_content = b'Hello World'
        s3.Object(config.s3_bucket, key_name).put(Body=file_content)
    except Exception:
        error = str(Exception)
    finally:
        flag_saved = False
        for bucket_object in bucket.objects.all():        
            if bucket_object.key == key_name:
                flag_saved = True
        if flag_saved:
            test_log.Add(test_name, 'GRANTED')
        else:
            test_log.Add(test_name, 'FAILED', str(error))

    # delete objects
    test_name = 'Deleting objects permission:'
    try:
        s3.Object(config.s3_bucket, key_name).delete()
    except Exception:
        error = str(Exception)
    finally:
        flag_deleted = False
        for bucket_object in bucket.objects.all():        
            if bucket_object.key == key_name:
                flag_deleted = True
        if not flag_deleted:
            test_log.Add(test_name, 'GRANTED')
        else:
            test_log.Add(test_name, 'FAILED', str(error))


    test_log.Show()
    




