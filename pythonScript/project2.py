import sublime
import sublime_plugin
import string

class project2(sublime_plugin.TextCommand):
  def isIdentifier(self,lexeme):
    if(len(lexeme) is 0):
      return False
    if (len(lexeme) > 0) and not lexeme[0].isalpha() :
      return False
    else:
      for i in lexeme:
        if not (i.isalpha() or i.isdigit() or (i is '_')):
          return False
    return True
  def extractSentence(line):
    return
  def functionCompleter(self,pos,word,line,initialSqOpen,initialCurlyOpen):
    sqOpen = initialSqOpen
    curlyOpen = initialCurlyOpen
    while True:
      if(line[pos] is '['):
        sqOpen+=1
      if(line[pos] is '('):
        curlyOpen+=1
      if(line[pos] is ']'):
        sqOpen-=1
      if(line[pos] is ')'):
        curlyOpen-=1
      word += line[pos]
      pos+=1
      if(pos >= len(line) or (sqOpen <= initialSqOpen and curlyOpen <= initialSqOpen) ):
        reserveWords = ["false ","true ","void ","vi ","vpii ","auto ","bool ","char ","double ","float ","int ","ll ","lld ","pii ","string "]
        for i in reserveWords:
          word = word.replace(i,"")
        return word
    return word
  def arrayCompleter(self,pos,word,line,initialSqOpen,initialCurlyOpen):
    sqOpen = 0
    curlyOpen = 0
    # print("len of initialCurlyOpen ",initialCurlyOpen)
    # print("len of initialSqOpen ",initialSqOpen)
    while True:
      if(line[pos] is '['):
        sqOpen+=1
      if(line[pos] is '('):
        curlyOpen+=1
      if(line[pos] is ']'):
        sqOpen-=1
      if(line[pos] is ')'):
        curlyOpen-=1
      word += line[pos]
      pos+=1
      # print("len of curlyOpen ",curlyOpen)
      # print("len of sqOpen ",sqOpen)
      # print("pos ",pos," line[pos] ",line[pos])
      if(sqOpen < 0 or curlyOpen < 0):
        return word[:-1]
      if(pos >= len(line) or (line[pos] in [' ',',',';','+','-','*','/','%','=',':','>','<',')','('] and sqOpen <= initialSqOpen and curlyOpen <= initialCurlyOpen) ):
        return word
    return word
  def isBalanced(self,lastWord):
    pos = len(lastWord) - 1
    sqOpen = 0
    curlyOpen = 0
    while pos >= 0:
      if(lastWord[pos] is ']'):
        sqOpen-=1
      elif(lastWord[pos] is '['):
        sqOpen+=1
      elif(lastWord[pos] is '('):
        curlyOpen+=1
      elif(lastWord[pos] is ')'):
        curlyOpen-=1
      pos-=1
    if(sqOpen is 0 and curlyOpen is 0):
      return True
    return False
  def splitIt(self,line):
    res = []
    lastWord = ""
    pos = 0
    sqOpen = 0
    curlyOpen = 0
    for i in line:
      # print("curly ",curlyOpen," sqOpen ",sqOpen)
      if(i in ['{','}']):
        pos+=1
        continue
      if(i in [' ',';']):
        if(lastWord in ["break","continue","return","and","or","bool","pii","vi","vpii","int","float","double","lld","ll","string","true","false","cout","cin","endl","newline","while","for","if","else","auto","void"]):
          lastWord = ""
        else:
          if(self.isIdentifier(lastWord)):
            res.append(lastWord)
          lastWord = ""
        curlyOpen = 0
        sqOpen = 0
      elif(i in ['(']):
        if(lastWord in ["if","else","for","do","while","rep","printf","scanf","memset","for","randVar","repd","repi","revd","setprecision"]):
          lastWord = ""
          curlyOpen = 0
          sqOpen = 0
        elif (lastWord in ["double","int","float","char"]):
          lastWord = ""
          sqOpen = 0
          curlyOpen = 0
        elif(pos < len(line) and (len(lastWord) is 0 or self.isIdentifier(lastWord)) ):
          lastWord = self.functionCompleter(pos,lastWord,line,sqOpen,curlyOpen)
          res.append(lastWord)
          lastWord = ""
          sqOpen = 0
          curlyOpen = 0
        else :
            lastWord = lastWord + i
            curlyOpen += 1
      elif(i in ['[']):
        # print("in[ ",lastWord)
        if(pos < len(line) and self.isIdentifier(lastWord)):
          lastWord = self.arrayCompleter(pos,lastWord,line,sqOpen,curlyOpen)
          # print("before append[ ",lastWord)
          res.append(lastWord)
          lastWord = ""
          sqOpen = 0
          curlyOpen = 0
        else :
            sqOpen += 1
      elif(i is ')'):
        curlyOpen-=1
        if(curlyOpen is 0):
          lastWord = lastWord + i
          res.append(lastWord)
          lastWord = ""
          sqOpen = 0
          curlyOpen = 0
      elif(i is ']'):
        # print("in] ",lastWord)
        # print(self.isBalanced(lastWord + ']'))
        if(not self.isBalanced(lastWord + ']')):
          # print("before append] ",lastWord)
          res.append(lastWord)
          lastWord = ""
          sqOpen = 0
          curlyOpen = 0
      elif(i in ['=',':',' ','+','/','-','*',';',',','%','>','<']):
        if(self.isIdentifier(lastWord)):
          res.append(lastWord)
        lastWord = ""
        sqOpen = 0
        curlyOpen = 0
      else:
        lastWord = lastWord + i
        # print(" lastWord ",lastWord)
      pos+=1
    if(self.isIdentifier(lastWord) and lastWord not in ["else"]):
      res.append(lastWord)
    return res
  def handelLine(self,line,uniqueWords):
    words = self.splitIt(line)
    res = ""
    for i in words:
      if(i not in uniqueWords):
        i = i.replace("++","")
        i = i.replace("--","")
        res = res + i + ','
        uniqueWords.add(i)
    if(len(res) > 0):
      res = res[:-1]
      res = "trace(" + res + ')'
    return res
  def detectIndentationLevel(self,line):
    res = 0
    for i in line:
      if i is not ' ':
        break
      res = res + 1
    return res
  def run(self, edit):
    for region in self.view.sel():
      if region.empty():
        sublime.status_message("empty line")
      else:
        lines = ((self.view.substr(region))[:-1]).split('\n')
        res = ""
        indextation = 0
        rows,cols = self.view.rowcol(region.begin())
        uniqueWords = set([""])
        for i in lines:
          indextation = self.detectIndentationLevel(i)
          message = self.handelLine(i.lstrip().rstrip(),uniqueWords)
          if(len(message) > 0):
            res = (' ' * indextation )  + message + '\n'
            #
            # rows + 1 because I want the line under selection line
            #
            pointTextToBeInserted = self.view.text_point(rows+1, 0)
            self.view.insert(edit, pointTextToBeInserted, res)
            rows = rows + 2
          else:
            rows = rows + 1
            # res = res + (' ' * indextation )  + message + '\n'
        # self.view.insert(edit, region.begin(), res)
