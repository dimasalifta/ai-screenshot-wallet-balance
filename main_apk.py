from kivy.app import App  
from kivy.uix.boxlayout import BoxLayout  
from kivy.uix.label import Label  
from kivy.clock import Clock  
from watchdog.observers import Observer  
from watchdog.events import FileSystemEventHandler  
import os  
from plyer import uniqueid, platform  
  
class ScreenshotHandler(FileSystemEventHandler):  
    def __init__(self, label, device_info):  
        self.label = label  
        self.device_info = device_info  
  
    def on_created(self, event):  
        # Memeriksa apakah file yang baru dibuat adalah screenshot  
        if event.is_directory:  
            return  
        if event.src_path.endswith('.png') or event.src_path.endswith('.jpg'):  
            screenshot_name = os.path.basename(event.src_path)  
            self.label.text = f'Screenshot baru dari {self.device_info}: {screenshot_name}'  
  
class MyApp(App):  
    def build(self):  
        layout = BoxLayout(orientation='vertical')  
        self.label = Label(text='Menunggu screenshot...')  
          
        # Mendapatkan informasi identitas perangkat  
        device_id = uniqueid.id  
        device_platform = platform.platform  
        self.device_info = f'ID Perangkat: {device_id}, Platform: {device_platform}'  
  
        layout.add_widget(self.label)  
  
        # Memulai pemantauan folder DCIM  
        self.start_monitoring()  
  
        return layout  
  
    def start_monitoring(self):  
        path = '/storage/emulated/0/DCIM'  
        event_handler = ScreenshotHandler(self.label, self.device_info)  
        self.observer = Observer()  
        self.observer.schedule(event_handler, path, recursive=False)  
        self.observer.start()  
  
        # Menghentikan observer saat aplikasi ditutup  
        self.bind(on_stop=self.stop_monitoring)  
  
    def stop_monitoring(self, *args):  
        self.observer.stop()  
        self.observer.join()  
  
if __name__ == '__main__':  
    MyApp().run()  
