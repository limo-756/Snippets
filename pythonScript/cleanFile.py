import sublime
import sublime_plugin


class cleanFile(sublime_plugin.TextCommand):
  def run(self, edit):
    deletedLines = []
    line_count = self.view.rowcol(self.view.size())[0] + 1
    # print("line_count",line_count)
    for i in range(0,line_count):
      pt = self.view.text_point(i,0)
      pt1 = self.view.full_line(pt)
      currLine = self.view.substr(pt1)
      # if(i == 402):
      #   print("hurray ",currLine)
      j = 0
      while j < len(currLine) and (currLine[j] is ' ' or currLine[j] is '\t'):
        j = j + 1
      # if(i == 402):
      #   print(currLine[j:j+6])
      if(j < len(currLine) and currLine[j:j+6] == "trace("):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+7] == "freopen"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+9] == "printBits"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+6] == "priArr"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+8] == "pri2DArr"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+6] == "priVec"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+8] == "pri2DVec"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+7] == "priCont"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+8] == "dfsPrint"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+13] == "priBinaryTree"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+10] == "priSegTree"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+7] == "priTrie"):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+70] == '#include "/home/anurag/desktop/program/codeForces/templates/MYLIB.cpp"'):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+74] == '#include "/home/anurag/desktop/program/codeForces/templates/RANDOMIZE.cpp"'):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+69] == '#include "/home/anurag/desktop/program/codeForces/templates/TEST.cpp"'):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+68] == '#include "/home/anurag/desktop/program/codeForces/templates/MEM.cpp"'):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+75] == 'freopen("/home/anurag/desktop/program/earth/contest/input.txt", "r", stdin)'):
        deletedLines += [i]
      elif(j < len(currLine) and currLine[j:j+2] == '//'):
        deletedLines += [i]
    print("deletedLines",deletedLines)
    num = 0
    for i in deletedLines:
      a = self.view.text_point(i - num,0)
      b = self.view.text_point(i+1 - num,0) -1
      rg = sublime.Region(a-1, b)
      self.view.erase(edit,rg)
      num = num +1