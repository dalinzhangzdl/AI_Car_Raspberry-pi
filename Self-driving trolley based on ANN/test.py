import time
import sys
import io
import glob
import configuration
from predict import Predictor
#import helpers.motor_driver as motor_driver_helper
#import helpers.image as image_helper

def main():
    model = None
    if len(sys.argv) > 1:
        model = sys.argv[1]
        print 'model load success'
    
    predictor = Predictor(model)

    for filename in glob.glob('./test_dataset/*'):
  
        direction = predictor.predict(filename)#stream)

        print direction

if __name__ == '__main__':
    main()
