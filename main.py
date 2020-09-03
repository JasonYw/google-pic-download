import json
import baiduspy
import googlespy



def readconfig(filename='example-config.json'):
    baidulist=[]
    googlelist=[]
    with open(filename,'r') as target:
        try:
            for line in target.readlines():
                config =json.loads(line)
                try:
                    if config['key'] ==None:
                        print('缺少关键字')
                        continue
                    if config['spider'].lower() == 'baidu':
                        baidulist.append(config['key'])
                        print('reading-config','spider:baidu','key:',config['key'])
                        continue
                    if config['spider'].lower() =='google':
                        googlelist.append(config['key'])
                        print('reading-config','spider:google','key:',config['key'])
                        continue
                except:
                    baidulist.append(config['key'])
                    googlelist.append(config['key'])
                    print('reading-config','spider:google & baidu','key:',config['key'])
        except Exception as e:
            print(e)
    
    if len(baidulist):
        for i in baidulist:
            baiduspy.main(i)
        
    if len(googlelist):
        for i in googlelist:
            googlespy.main(i)
                
def main():
    readconfig()

if __name__ == "__main__":
    main()

