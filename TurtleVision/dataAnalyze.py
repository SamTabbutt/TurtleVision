#This file is to handle all deep learning development and analysis. It is currently in its first stage
#I need to bush up on my linear algebra before making this functional

import numpy as np
import mxnet as mx
from mxnet import nd, autograd, gluon
from mxnet.gluon.data.vision import transforms as trans
import pickle      #included in python 3
import base64      #included in python 3
from PIL import Image
import gc
import time

from .models import Frame, tag, learningModel, tagAssign


ctx = mx.gpu() if mx.test_utils.list_gpus() else mx.cpu()
data_ctx = ctx
model_ctx = ctx

batch_size = 30
num_inputs = 195075
num_outputs = 2

num_examples = 380

#import dataset as list of Frame instances

#normalize dataset and organize into 
#list of tuples?

#adapted from https://gluon.mxnet.io/chapter04_convolutional-neural-networks/cnn-gluon.html

def evaluate_accuracy(data_iterator, net):
    acc = mx.metric.Accuracy()
    for i, (data, label) in enumerate(data_iterator):
        data = data.as_in_context(model_ctx).reshape((0,num_inputs))
        print(data.shape)
        label = label.as_in_context(model_ctx)
        output = net(data)
        predictions = nd.argmax(output, axis=1, keepdims=True)
        acc.update(preds=predictions, labels=label)
    return acc.get()[1]

class initiateModel():
	def __init__(self, anal_type):
		self.type=anal_type

	def createDataArray(self):
		gc.collect()
		#Change for modulation. Doing only for current configuration
		anal_type_frames = Frame.objects.all().filter(tag__tag_type__pk=self.type.pk)

		train_data =[]
		train_label =[]

		for frame in anal_type_frames:
			im = frame.imgData
			np_bytes = base64.b64decode(im)
			np_array = pickle.loads(np_bytes)

			image_out=nd.array(np_array)

			label = frame.tag.tag_num-1
			enter_label = nd.array([label])
			train_data.append(image_out)
			train_label.append(enter_label)
		train_data_set = gluon.data.ArrayDataset(train_data,train_label)
		data = gluon.data.DataLoader(train_data_set, batch_size, shuffle=False)
		return data


	def defineAndTrainModel(self, train_data):
		net = gluon.nn.Dense(num_outputs)
		net.collect_params().initialize(mx.init.Normal(sigma=1.), ctx=model_ctx)
		softmax_cross_entropy = gluon.loss.SoftmaxCrossEntropyLoss()
		trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate': 0.1})

		print(evaluate_accuracy(train_data, net))
		
		epochs = 10
		moving_loss = 0.

		for e in range(epochs):
			cumulative_loss = 0
			for i, (data, label) in enumerate(train_data):
				data = data.as_in_context(model_ctx).reshape((0,num_inputs))
				label = label.as_in_context(model_ctx)
				with autograd.record():
					output = net(data)
					loss = softmax_cross_entropy(output, label)
				loss.backward()
				trainer.step(batch_size)
				cumulative_loss += nd.sum(loss).asscalar()

			train_accuracy = evaluate_accuracy(train_data, net)
			print("Epoch %s. Loss: %s, Train_acc %s" % (e, cumulative_loss/num_examples, train_accuracy))

		
		newModel = learningModel(tag_type=self.type, parameters_dir='')
		file_path = 'C:/Users/samta/TurtleCam/media/models/' + 'testing' +'.params'
		newModel.parameters_dir = file_path
		newModel.save()

		net.save_parameters(file_path)
		
		
#creating instances this way assuming that batching isn't as important when applying the model
#more updates. for now going to create  pseudo-code
class applyModel():
	def __init__(self, anal_type, file_path, ses):
		self.type = anal_type
		self.session = ses
		self.path = file_path
		self.net = gluon.nn.Dense(num_outputs)
		print(self.path)
		self.net.load_parameters(self.path, ctx=ctx)

	def saveSecond(self,nd_img, sec, second):
		print(str(sec)+" img shape:")
		print(nd_img.shape)
		reshaped = nd_img.as_in_context(model_ctx).reshape((1,num_inputs))
		print(reshaped.shape)
		output = self.net(reshaped)
		print(output)
		pred = nd.argmax(output, axis=1, keepdims=True)
		print("0 for breath 1 for apnea:")
		print(pred)
		pred_np = pred.asnumpy()
		
		guess_val = pred_np[0,0]+1

		print(guess_val)
		
		get_tag = tag.objects.all().get(tag_num=guess_val)
		
		thisModelSet = learningModel.objects.filter(parameters_dir = self.path).order_by('-create_date_time')

		print(thisModelSet)

		thisModel=thisModelSet[0]

		print(thisModel)

		newTag = tagAssign(tag = get_tag, accuracy=0, assigned_by= thisModel)
		
		#newTag.save()

		#second.tag.add(newTag)

		print("done")
		
		return