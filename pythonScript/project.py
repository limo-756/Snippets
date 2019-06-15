import sublime
import sublime_plugin


class addLib(sublime_plugin.TextCommand):
    def run(self, edit):
      list = [False,False,False,False]
      line_count = self.view.rowcol(self.view.size())[0] + 1
      mainLine = -1
      for i in range(0,line_count):
        pt = self.view.text_point(i,0)
        pt1 = self.view.full_line(pt)
        currLine = self.view.substr(pt1)
        j = 0
        while j < len(currLine) and (currLine[j] is ' ' or currLine[j] is '\t'):
          j = j + 1
        if(j < len(currLine) and currLine[j:j+70] == '#include "/home/anurag/desktop/program/codeForces/templates/MYLIB.cpp"'):
          list[0] = True
        elif(j < len(currLine) and currLine[j:j+74] == '#include "/home/anurag/desktop/program/codeForces/templates/RANDOMIZE.cpp"'):
          list[1] = True
        elif(j < len(currLine) and currLine[j:j+69] == '#include "/home/anurag/desktop/program/codeForces/templates/TEST.cpp"'):
          list[2] = True
        elif(j < len(currLine) and currLine[j:j+76] == 'freopen("/home/anurag/desktop/program/earth/contest/input.txt", "r", stdin);'):
          list[3] = True
        elif(j < len(currLine) and currLine[j:j+38] == 'int main(int argc, char const *argv[])'):
          if(i+1 < line_count):
            pt = self.view.text_point(i+1,0)
            pt1 = self.view.full_line(pt)
            currLine = self.view.substr(pt1)
            if(currLine[0:1] == "{"):
              pt = self.view.text_point(i+2,0)
              pt1 = self.view.full_line(pt)
              currLine = self.view.substr(pt1)
              if(currLine.strip() == "ios_base::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL);"):
                mainLine = i+3
        elif(j < len(currLine) and currLine[j:j+39] == 'int main(int argc, char const *argv[]){'):
          mainLine = i+1
        elif(j < len(currLine) and currLine[j:j+39] == 'int main(int argc, char const *argv[]) {'):
          mainLine = i+1
        elif(j < len(currLine) and currLine[j:j+39] == 'int main() {'):
          mainLine = i+1
        elif(j < len(currLine) and currLine[j:j+39] == 'int main(){'):
          mainLine = i+1
      pt = self.view.text_point(86,0)
      if(line_count < 140):
        pt = self.view.text_point(0,0)
      if(list[0] == False):
        mainLine = mainLine + 1
        self.view.insert(edit, pt, '#include "/home/anurag/desktop/program/codeForces/templates/TEST.cpp"\n')
      if(list[1] == False):
        mainLine = mainLine + 1
        self.view.insert(edit, pt, '#include "/home/anurag/desktop/program/codeForces/templates/RANDOMIZE.cpp"\n')
      if(list[2] == False):
        mainLine = mainLine + 1
        self.view.insert(edit, pt, '#include "/home/anurag/desktop/program/codeForces/templates/MYLIB.cpp"\n')
      if(list[3] == False and mainLine != -1 and mainLine != 2):
        pt = self.view.text_point(mainLine,0)
        self.view.insert(edit, pt, '  freopen("/home/anurag/desktop/program/earth/contest/input.txt", "r", stdin);\n')

