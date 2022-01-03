import random
import warnings

# import tensorflow as tf
import numpy as np
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView
from rest_framework.response import Response

from patients.models import Patient
from testtype.models import TestType
from .models import SampleData
from .serializer import ResultSerializer, ImageDataSerializer, SampleDataSerializer

# import tensorflow as tf
#
# tf.keras.backend.clear_session()
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model

warnings.filterwarnings('ignore', category=UserWarning, module='skimage')

model = None

IMG_WIDTH = 512
IMG_HEIGHT = 512
IMG_CHANNELS = 1

seed = 42
random.seed = seed
np.random.seed(0)
sizes_test = []


# class ImageModel:
#     def pre_load_model(self):
#         global model
#         model = load_model(
#             r'/home/wappnet01/Harsh/officeworkspace/medical_iot/imageprediction/samplemodel/model-POSITIVE-198-1.h5',
#             compile=False)
#         model._make_predict_function()
#         print(model.summary())
#
#     def rle_encoding(self, x):
#         dots = np.where(x.T.flatten() == 1)[0]
#         run_lengths = []
#         prev = -2
#         for b in dots:
#             if (b > (prev + 1)):
#                 run_lengths.extend((b + 1, 0))
#                 run_lengths[-1] += 1
#                 prev = b
#         return run_lengths
#
#     def prob_to_rles(self, x, cutoff=0.3):
#         lab_img = label(x > cutoff)
#         for i in range(1, lab_img.max() + 1):
#             yield self.rle_encoding(lab_img == i)
#
#     def prepare_image(self, image, target):
#         if image.mode != "RGB":
#             image = image.convert("RGB")
#
#         print(image.size)
#         image = image.resize(target)
#         image = img_to_array(image)
#         return image


# Create your views here.
class ImagePredection(APIView):
    def modify_input_for_multiple_files(self, image, result_length, result, last_sample_id):
        dict = {}
        dict['image_name'] = image
        dict['result_length'] = result_length
        dict['result'] = result
        dict['sample_data_id'] = last_sample_id
        return dict

    def post(self, request):
        if request.data['mode'] == 'autoscope':
            if Patient.objects.filter(patient_email=request.data['patient_email']).exists():
                if TestType.objects.filter(disease_name=request.data['disease_name']).exists():
                    # imgobj = ImageModel()
                    images = dict((request.data).lists())['image']
                    my_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
                    user_id = Token.objects.get(key=my_token).user_id
                    patient_id = Patient.objects.get(patient_email=request.data['patient_email']).id
                    test_type = TestType.objects.get(disease_name=request.data['disease_name']).id
                    data = {'mode': request.data['mode'], 'test_type': test_type, 'patient_id': patient_id,
                            'user_id': user_id}
                    serializer_class = SampleDataSerializer(data=data)
                    if serializer_class.is_valid():
                        serializer_class.save()
                        last_sample_id = SampleData.objects.filter(mode=request.data['mode'], test_type=test_type,
                                                                   patient_id=patient_id, user_id=user_id).last().id
                    else:
                        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

                    # file = request.FILES['image']
                    # image = file.read()
                    # image = Image.open(io.BytesIO(image))
                    #
                    # image = imgobj.prepare_image(image, target=(512, 512))
                    # X_test = image[:, :, 0]
                    # X_test3 = np.expand_dims(X_test, axis=0)
                    # X_test2 = np.expand_dims(X_test3, axis=3)
                    #
                    # imgobj.pre_load_model()
                    # preds_test = model.predict(X_test2)
                    #
                    # preds_test_t = (preds_test > 0.3).astype(np.uint8)
                    # print(preds_test_t)
                    #
                    # sizes_test.append([image.shape[0], image.shape[1]])
                    # preds_test_upsampled = resize(np.squeeze(preds_test), sizes_test[0], mode='constant',
                    #                               preserve_range=True)
                    #
                    # test_rle = list(imgobj.prob_to_rles(preds_test_upsampled))
                    # print(len(test_rle))

                    flag, negative = True, True
                    for image_name in images:
                        """
                        dummy
                        """
                        temp = ["Positive", "Negative", "Grade 1", "Grade 2", "Grade 3"]
                        result_length = random.randint(0, 1024)
                        result = random.choice(temp)
                        """
                        dummy ends
                        """
                        modified_data = self.modify_input_for_multiple_files(image_name, result_length, result,
                                                                             last_sample_id)
                        serializer_class = ImageDataSerializer(data=modified_data)
                        if serializer_class.is_valid():
                            if modified_data['result'] != 'Negative':
                                print('here')
                                print(last_sample_id)
                                SampleData.objects.filter(id=last_sample_id).update(
                                    result=modified_data['result'])
                                negative = False
                            serializer_class.save()
                        else:
                            flag = False

                    if flag == True:
                        if negative == True:
                            SampleData.objects.filter(id=last_sample_id).update(
                                result='Negative')
                        return Response({"status": True, "msg": "Successfully uploaded sample"},
                                        status=status.HTTP_200_OK)
                    else:
                        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status": False, "msg": "Disease name Not Exist"})
            else:
                return Response({"status": False, "msg": "Patient Not Exist"})
        elif request.data['mode'] == 'ace_it':
            if Patient.objects.filter(patient_email=request.data['patient_email']).exists():
                if TestType.objects.filter(disease_name=request.data['disease_name']).exists():
                    my_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
                    user_id = {"user_id": Token.objects.get(key=my_token).user_id}
                    patient_id = {"patient_id": Patient.objects.get(patient_email=request.data['patient_email']).id}
                    test_type = {"test_type": TestType.objects.get(disease_name=request.data['disease_name']).id}
                    """
                    dummy
                    """
                    temp = ["Positive", "Negative", "Grade 1", "Grade 2", "Grade 3"]
                    test_rle = random.randint(0, 1024)
                    result = {'result': random.choice(temp)}
                    """
                    dummy ends
                    """
                    image_name = {'image_name': 'ACE_IT-Test-no_image'}
                    # result_length = {'result_length': len(test_rle)}
                    result_length = {'result_length': test_rle}

                    request.data._mutable = True
                    request_image_name = image_name
                    request_length = result_length
                    request_user = user_id
                    request_patient_id = patient_id
                    request_test_type = test_type
                    request.data.update(request_image_name)
                    request.data.update(request_length)
                    request.data.update(result)
                    request.data.update(request_test_type)
                    request.data.update(request_patient_id)
                    request.data.update(request_user)

                    serializer_class = SampleDataSerializer(data=request.data)
                    if serializer_class.is_valid():
                        serializer_class.save()
                        return Response({"status": True, "msg": "Successfully uploaded sample"},
                                        status=status.HTTP_200_OK)
                    return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status": False, "msg": "Disease name Not Exist"})
            else:
                return Response({"status": False, "msg": "Patient Not Exist"})

    def get(self, request):
        results = SampleData.objects.all()
        serializer_class = ResultSerializer(results, many=True)
        return Response(serializer_class.data)
