from alpa.model.GameDB import Game

# class Logger(object):
#   def __init__(self, filename="Default.log"):
#     self.terminal = sys.stdout
#     self.log = open(filename, "a")
#   def write(self, message):
#     self.terminal.write(message)
#     try:
#         self.log.write(message)
#     except Exception as e:
#         print('error')
#   def flush(self):
#     pass

# path = os.path.abspath(os.path.dirname(__file__))
# type = sys.getfilesystemencoding()
# sys.stdout = Logger('a.txt')

# os.system("python ./code/TAPTAP发现.py")
# os.system("python ./code/TAPTAP榜单.py")
# os.system("python ./code/GameRes90天榜单.py")
# os.system("python ./code/GameRes开测表.py")
# os.system("python ./code/9Game预约榜.py")
# os.system("python ./code/9Game开测表.py")

Game('gamedb', 'detail').outputfollow('name',['偶像不是人','武林闲侠'])