import onnx
import onnxruntime as ort
import numpy as np
import json
import os
import sys
import time

from PIL import Image, ImageDraw, ImageFont, ImageOps


def load_labels(path):
    with open(path) as f:
        data = json.load(f)
    return np.asarray(data)

# Run the model on the backend
d=os.path.dirname(os.path.abspath(__file__))
modelfile=os.path.join(d , 'model3.onnx')
labelfile=os.path.join(d , 'labels.json')
#print(d)
labels = load_labels(labelfile)
#print(labels)
ort_sess = ort.InferenceSession(modelfile,  providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'])


def preprocess(input_data):
    img_data = np.array(input_data).astype('float32')
    # convert the input data into the float32 input
    #img_data = input_data.astype('float32')
    #print(img_data.shape)
    #normalize
    mean_vec = np.array([0.485, 0.456, 0.406])
    stddev_vec = np.array([0.229, 0.224, 0.225])
    norm_img_data = np.zeros(img_data.shape).astype('float32')
    for i in range(img_data.shape[0]):
        norm_img_data[i,:,:] = (img_data[i,:,:]/255 - mean_vec[i]) / stddev_vec[i]

    #add batch channel
    norm_img_data = norm_img_data.reshape(1,3,224, 224).astype('float32')
    return norm_img_data

def softmax(x):
    x = x.reshape(-1)
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def postprocess(result):
    return softmax(np.array(result)).tolist()


def predict_image_from_file(img_path):
    """
    img_path : the location of the image file to be processed
    This functiion re-shape the input image, normalize the input

    """
    image = Image.open(img_path)

    imnew=ImageOps.fit(image, (224,224))

    image_data = np.array(imnew).transpose(2, 0, 1)
    input_data = preprocess(image_data)
    #print(input_data.shape)
    #print("********************************************************")
    start = time.time()
    raw_result = ort_sess.run(None, {'input':input_data})
    end = time.time()
    #print("********************************************************")

    #print(raw_result)
    res = postprocess(raw_result)

    inference_time = np.round((end - start) * 1000, 2)
    idx = np.argmax(res)

    response = {
            'prediction': labels[idx],
            'latency': inference_time,
            'confidence': res[idx]
    }

    return response


if __name__ == '__main__':
    path = os.path.join(d, '94974-cat-animals-Russia.jpg')
    print(predict_image_from_file(path))


    
    
"""

path = os.path.join(d, '94974-cat-animals-Russia.jpg')


print(predict_image(path))

"""
