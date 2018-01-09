# lazyimporter
lazyimporter
import py的文件，延时加载，针对项目中用py文件data的情况

例如aa_data.py, 内容是
data={1: 10001, 
2:10002}


那么import lazyimporter之后 ，import aa_data

只有在首次使用aa.data[1]才真正import
