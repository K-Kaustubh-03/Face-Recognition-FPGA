import json

dataWidth = 32
dataIntWidth = 1
weightIntWidth = 4
inputFile = "Distances.txt"
dataFracWidth = dataWidth-dataIntWidth
weightFracWidth = dataWidth-weightIntWidth
biasIntWidth = dataIntWidth+weightIntWidth
biasFracWidth = dataWidth-biasIntWidth
outputPath = "./w_b/"
headerPath = "./"

def DtoB(num,dataWidth,fracBits):						#funtion for converting into two's complement format
	if num >= 0:
		num = num * (2**fracBits)
		num = int(num)
		d = num
	else:
		num = -num
		num = num * (2**fracBits)		#number of fractional bits
		num = int(num)
		if num == 0:
			d = 0
		else:
			d = 2**dataWidth - num
	return d

def genWaitAndBias(dataWidth,weightFracWidth,biasFracWidth,inputFile):
	weightIntWidth = dataWidth-weightFracWidth
	biasIntWidth = dataWidth-biasFracWidth
	myDataFile = open(inputFile,"r")
	weightHeaderFile = open(headerPath+"distancesValues.h","w")
	myData = myDataFile.read()
	myDict = json.loads(myData)
	myWeights = myDict['distances']
	weightHeaderFile.write("int distancesValues[]={")
	for layer in range(0,len(myWeights)):
		for neuron in range(0,len(myWeights[layer])):
			fi = 'd_'+str(layer+1)+'_'+str(neuron)+'.mif'
			f = open(outputPath+fi,'w')
			for weight in range(0,len(myWeights[layer][neuron])):
				if 'e' in str(myWeights[layer][neuron][weight]):
					p = '0'
				else:
					if myWeights[layer][neuron][weight] > 2**(weightIntWidth-1):
						myWeights[layer][neuron][weight] = 2**(weightIntWidth-1)-2**(-weightFracWidth)
					elif myWeights[layer][neuron][weight] < -2**(weightIntWidth-1):
						myWeights[layer][neuron][weight] = -2**(weightIntWidth-1)
					wInDec = DtoB(myWeights[layer][neuron][weight],dataWidth,weightFracWidth)
					p = bin(wInDec)[2:]
				f.write(p+'\n')
				weightHeaderFile.write(str(wInDec)+',')
			f.close()
	weightHeaderFile.write('0};\n')
	weightHeaderFile.close()
			
if __name__ == "__main__":
	genWaitAndBias(dataWidth,weightFracWidth,biasFracWidth,inputFile)