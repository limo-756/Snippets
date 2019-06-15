import sublime
import sublime_plugin


class secret(sublime_plugin.TextCommand):
  def run(self, edit):
    sublime.Window.open_file(sublime.active_window(),"/media/anurag/20781584781559BC/Users/Anurag/Documents/default/dep/system/girls")
