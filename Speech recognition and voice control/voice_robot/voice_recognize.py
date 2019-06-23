#_*_ coding:UTF-8 _*_
# @author: zdl 
# 对本地录音文件进行语音识别，将识别结果保存至txt文本中，对txt文本进行语音合成生成mp3文件


# 导入AipSpeech  AipSpeech是语音识别的Python SDK客户端
from aip import AipSpeech



''' 你的APPID AK SK  参数在申请的百度云语音服务的控制台查看'''
APP_ID = '11472625'
API_KEY = 'NYIvd23qqGAZ1ZPpVpCthENs'
SECRET_KEY = 'DcQWQ9HVc0sqoD091gFxWiCP1i0oNa6u'

# 新建一个AipSpeech
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
  
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件并合成
def identify_synthesize(fileName):
    result = client.asr(get_file_content(fileName), 
			    'wav', 16000, 
			    {'dev_pid': 1536,})
    print result

    if result['err_msg']=='success.':
        word = result['result'][0].encode('utf-8')   # 编码utf-8
        if word!='':
            if word[len(word)-3:len(word)]=='，':
                print word[0:len(word)-3]
                with open('result.txt','w') as f:
                    f.write(word[0:len(word)-3])
                f.close()
            else:
                print (word.decode('utf-8'))
                with open('result.txt','w') as f:
                    f.write(word)
                f.close()
        else:
            print "音频文件不存在或格式错误"
    else:
        print "错误"
        with open('result.txt','w') as f:
            f.write('语音识别错误')
        f.close()

    
    # 打开文件，读取文件内容
    f = open('result.txt','r')
    command = f.read()
    if len(command) != 0:
        word = command
    f.close()
    # 语音合成
    result  = client.synthesis(word ,'zh',1, {
        'vol': 5,'per':0,
    })
	
# 语音合成正确则返回audio.mp3 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('synthesis.mp3', 'wb') as f:
            f.write(result)
        f.close()
    

if __name__ == '__main__':

    identify_synthesize('yahboom.wav')
	
