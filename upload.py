from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

class upload:
    def upload_photo(self,yesterday):
        file_date = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]
        date = str(yesterday)[:4]+"-"+str(yesterday)[5:7]+"-"+str(yesterday)[8:10]
        graph_folder_id = '1DYMTmnR_aAB_hvBKBhIimqWQ73lvkr0r'

        #graph upload
        child_folder = drive.CreateFile({'title': f'{file_date}', 'mimeType':'application/vnd.google-apps.folder','parents':[{'id':f"{graph_folder_id}"}]})
        child_folder.Upload()
        print()
        for i in range(24):
            f = drive.CreateFile({'title': f'./{file_date}/BTCJPY_{file_date}_{i+1}.png',
                                'mimeType': 'image/png',
                                'parents': [{'kind': 'drive#fileLink', 'id':f"{child_folder['id']}"}]})
            f.SetContentFile(f'./graphs/BTCJPY_{file_date}_{i+1}.png')
            f.Upload()
            f = drive.CreateFile({'title': f'./{file_date}/BTCUSD_{file_date}_{i+1}.png',
                                'mimeType': 'image/png',
                                'parents': [{'kind': 'drive#fileLink', 'id':f"{child_folder['id']}"}]})
            f.SetContentFile(f'./graphs/BTCUSD_{file_date}_{i+1}.png')
            f.Upload()

