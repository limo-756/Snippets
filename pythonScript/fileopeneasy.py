import sublime
import sublime_plugin

class fileopeneasy(sublime_plugin.TextInputHandler):
  def run(self):
    var = self.input("poinrr")
    var.initial_text("goto :")
    var.placeholder("anurag : ")
    # self.window.show_input_panel("open file easy:", "Standard", self.on_done, None, None)

  def on_done(self, text):
    line = text
    if self.window.active_view():
      self.window.active_view().run_command("myhelper", {"line": line})


class myhelper(sublime_plugin.TextCommand):
  def run(self, edit):
    print("wroking")
    # self.view.name("anurag")
    var = sublime_plugin.TextCommand.input(self,sublime.active_window())
    # var.placeholder()