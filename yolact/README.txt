This project allows to train YOLACT on a custom dataset in order to perform hand segmentation.

Requirements : 
	Python 3.6 or higher
 	RHD hand dataset : https://lmb.informatik.uni-freiburg.de/resources/datasets/RenderedHandposeDataset.en.html

Annotations.py generates an COCO-like annotation JSON file.

Steps : 
	1) Generate the annotations file by running tojson_all(directory) in Python, with directory the folder containing all the hand mask images
	   There already is an example in yolact-master/data/training/RHD_published_v2/annotations made out of a 1044 images sized training set
	2) Install yolact :
		a)pip install cython
		b)pip install opencv-python pillow pycocotools matplotlib 
		c)Install PyTorch 1.0.1 or higher
		d)cd external/DCNv2
		  python setup.py build develop if you want to use YOLACT++

	3) Change the config.py file in yolact-master/data in order to create a new config matching with your dataset (see POC_YOLACT_Hand_Segmentation.pdf)
	4) In the cmd, change directory to yolact-master and run : python train.py --config=yolact_base_config (or yolact_im400_config if you don't have enough RAM on the GPU)
	5) Step 3 creates a weights file in yolact-master/weights; you can evaluate the trained model by running :
		a) python eval.py --trained_model=weights/your_trained_model.pth --score_threshold=0.15 --top_k=15 --image=my_image.png to evaluate on a specific image
		b) python eval.py --trained_model=weights/your_trained_model.pth --score_threshold=0.15 --top_k=15 --video_multiframe=4 --video=0 to evaluate on a webcam feed (replace 0 by the number of your webcam)

Note that by defining yolact_base_config on a specific dataset, you also define yolact_im400_config, yolact_plus_base_config etc on the same dataset.