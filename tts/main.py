import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import urllib.request
import urllib.parse
import hashlib
import json
import os
from datetime import datetime
import random
import time
import tempfile
import threading

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("警告: pygame 未安装，播放功能将不可用。请运行: pip install pygame")

class NanoAITTS:
    def __init__(self):
        self.name = '纳米AI'
        self.id = 'bot.n.cn'
        self.author = 'TTS Server'
        self.icon_url = 'https://bot.n.cn/favicon.ico'
        self.version = 2
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        self.voices = {}
        self.load_voices()
    
    def md5(self, msg):
        """MD5 哈希函数"""
        return hashlib.md5(msg.encode('utf-8')).hexdigest()
    
    def _e(self, nt):
        """生成哈希值"""
        HASH_MASK_1 = 268435455
        HASH_MASK_2 = 266338304
        
        at = 0
        for i in range(len(nt) - 1, -1, -1):
            st = ord(nt[i])
            at = ((at << 6) & HASH_MASK_1) + st + (st << 14)
            it = at & HASH_MASK_2
            if it != 0:
                at = at ^ (it >> 21)
        return at
    
    def generate_unique_hash(self):
        """生成唯一哈希"""
        lang = 'zh-CN'
        app_name = "chrome"
        ver = 1.0
        platform = "Win32"
        width = 1920
        height = 1080
        color_depth = 24
        referrer = "https://bot.n.cn/chat"
        
        nt = f"{app_name}{ver}{lang}{platform}{self.ua}{width}x{height}{color_depth}{referrer}"
        at = len(nt)
        it = 1
        while it:
            nt += str(it ^ at)
            it -= 1
            at += 1
        
        return (round(random.random() * 2147483647) ^ self._e(nt)) * 2147483647
    
    def generate_mid(self):
        """生成 MID"""
        domain = "https://bot.n.cn"
        rt = str(self._e(domain)) + str(self.generate_unique_hash()) + str(int(time.time() * 1000) + random.random() + random.random())
        formatted_rt = rt.replace('.', 'e')[:32]
        return formatted_rt
    
    def get_iso8601_time(self):
        """获取 ISO8601 时间格式"""
        now = datetime.now()
        return now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    def get_headers(self):
        """生成请求头"""
        device = "Web"
        ver = "1.2"
        timestamp = self.get_iso8601_time()
        access_token = self.generate_mid()
        zm_ua = self.md5(self.ua)
        
        zm_token_str = f"{device}{timestamp}{ver}{access_token}{zm_ua}"
        zm_token = self.md5(zm_token_str)
        
        return {
            'device-platform': device,
            'timestamp': timestamp,
            'access-token': access_token,
            'zm-token': zm_token,
            'zm-ver': ver,
            'zm-ua': zm_ua,
            'User-Agent': self.ua
        }
    
    def http_get(self, url, headers):
        """使用标准库发送 GET 请求"""
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"HTTP GET 请求失败: {e}")
    
    def http_post(self, url, data, headers):
        """使用标准库发送 POST 请求"""
        data_bytes = data.encode('utf-8')
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read()
        except Exception as e:
            raise Exception(f"HTTP POST 请求失败: {e}")
    
    def load_voices(self):
        """加载声音列表"""
        filename = 'robots.json'
        
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                response_text = self.http_get('https://bot.n.cn/api/robot/platform', self.get_headers())
                data = json.loads(response_text)
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 清空旧的声音列表
            self.voices.clear()
            for item in data['data']['list']:
                self.voices[item['tag']] = {
                    'name': item['title'],
                    'iconUrl': item['icon']
                }
        except Exception as e:
            print(f"加载声音列表失败: {e}")
            self.voices.clear()
            # 如果网络请求失败，添加默认选项
            self.voices['DeepSeek'] = {'name': 'DeepSeek (默认)', 'iconUrl': ''}
    
    def get_audio(self, text, voice='DeepSeek'):
        """获取音频"""
        url = f'https://bot.n.cn/api/tts/v1?roleid={voice}'
        
        headers = self.get_headers()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        form_data = f'&text={urllib.parse.quote(text)}&audio_type=mp3&format=stream'
        
        try:
            audio_data = self.http_post(url, form_data, headers)
            return audio_data
        except Exception as e:
            print(f"获取音频失败: {e}")
            raise

class AudioPlayer:
    """音频播放器类"""
    def __init__(self):
        # ✅ *** 修正点: 将 global 声明移到方法顶部 ***
        global PYGAME_AVAILABLE
        
        self.is_playing = False
        self.is_paused = False
        self.current_file = None
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
            except pygame.error as e:
                print(f"Pygame mixer 初始化失败: {e}")
                PYGAME_AVAILABLE = False
    
    def play(self, audio_data):
        if not PYGAME_AVAILABLE:
            raise Exception("Pygame 未安装或初始化失败，无法播放音频。")
        self.stop()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(audio_data)
            self.current_file = temp_file.name
        
        pygame.mixer.music.load(self.current_file)
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
    
    def pause(self):
        if PYGAME_AVAILABLE and self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
    
    def resume(self):
        if PYGAME_AVAILABLE and self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
    
    def stop(self):
        if PYGAME_AVAILABLE:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        if self.current_file:
            try:
                os.remove(self.current_file)
                self.current_file = None
            except OSError as e:
                print(f"删除临时文件失败: {e}")
    
    def is_busy(self):
        if PYGAME_AVAILABLE and self.is_playing:
            return pygame.mixer.music.get_busy()
        return False

class TTSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("纳米AI文字转语音工具")
        self.root.geometry("800x650")
        self.root.minsize(700, 600)
        
        self.bg_color = "#f5f7fa"
        self.primary_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.warning_color = "#FF9800"
        self.danger_color = "#F44336"
        self.text_color = "#333333"
        
        self.root.config(bg=self.bg_color)
        
        self.tts = NanoAITTS()
        self.player = AudioPlayer()
        
        self.setup_styles()
        self.setup_ui()
        
        self.check_playback_status()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff", foreground=self.text_color, arrowcolor="#666666", relief="flat", borderwidth=1)
        style.map("TCombobox", fieldbackground=[('readonly', '#ffffff')])
        
        style.configure("Modern.TButton", font=("微软雅黑", 11, "bold"), padding=(20, 12), relief="flat", borderwidth=0)
        style.map("Modern.TButton", foreground=[('!disabled', 'white')], background=[('disabled', '#e0e0e0')])
                       
        style.configure("Success.Modern.TButton", background=self.success_color)
        style.map("Success.Modern.TButton", background=[('active', '#45a049')])
        style.configure("Warning.Modern.TButton", background=self.warning_color)
        style.map("Warning.Modern.TButton", background=[('active', '#F57C00')])
        style.configure("Primary.Modern.TButton", background=self.primary_color)
        style.map("Primary.Modern.TButton", background=[('active', '#1976D2')])
        style.configure("Danger.Modern.TButton", background=self.danger_color)
        style.map("Danger.Modern.TButton", background=[('active', '#D32F2F')])
        style.configure("Secondary.Modern.TButton", background="#9E9E9E", padding=(15, 8), font=("微软雅黑", 10, "bold"))
        style.map("Secondary.Modern.TButton", background=[('active', '#757575')])

    def setup_ui(self):
        status_bar_frame = tk.Frame(self.root, bg="#e0e6ed", height=30)
        status_bar_frame.pack(side="bottom", fill="x")
        status_bar_frame.pack_propagate(False)
        self.status_icon = tk.Label(status_bar_frame, text="✓", font=("Arial", 12, "bold"), fg=self.success_color, bg="#e0e6ed")
        self.status_icon.pack(side="left", padx=(10, 5))
        self.status_label = tk.Label(status_bar_frame, text="就绪", font=("微软雅黑", 9), fg="#555555", bg="#e0e6ed", anchor="w")
        self.status_label.pack(side="left", fill="x", expand=True)

        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = tk.Frame(main_container, bg=self.bg_color)
        header_frame.pack(side="top", fill="x", pady=(0, 20))
        icon_label = tk.Label(header_frame, text="🎙️", font=("Arial", 32), bg=self.bg_color)
        icon_label.pack(side="left", padx=(0, 15))
        title_text_frame = tk.Frame(header_frame, bg=self.bg_color)
        title_text_frame.pack(side="left")
        tk.Label(title_text_frame, text="纳米AI文字转语音工具", font=("微软雅黑", 20, "bold"), fg=self.text_color, bg=self.bg_color).pack(anchor="w")
        tk.Label(title_text_frame, text="Text to Speech Converter", font=("Arial", 10), fg="#666666", bg=self.bg_color).pack(anchor="w")

        button_frame = tk.Frame(main_container, bg="#ffffff", bd=1, relief="solid", highlightbackground="#e0e0e0", highlightthickness=1)
        button_frame.pack(side="bottom", fill="x", pady=(15, 0))
        
        settings_frame = tk.Frame(main_container, bg="#ffffff", bd=1, relief="solid", highlightbackground="#e0e0e0", highlightthickness=1)
        settings_frame.pack(side="bottom", fill="x", pady=(15, 0))

        text_frame = tk.Frame(main_container, bg="#ffffff", bd=1, relief="solid", highlightbackground="#e0e0e0", highlightthickness=1)
        text_frame.pack(side="top", fill="both", expand=True)
        
        tk.Label(text_frame, text="📝 输入文本", font=("微软雅黑", 12, "bold"), fg=self.text_color, bg="#ffffff").pack(anchor="w", padx=15, pady=(15, 10))
        text_input_container = tk.Frame(text_frame, bg="#ffffff")
        text_input_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        scrollbar = tk.Scrollbar(text_input_container)
        scrollbar.pack(side="right", fill="y")
        self.text_input = tk.Text(text_input_container, wrap="word", font=("微软雅黑", 11), fg=self.text_color, relief="flat", bd=0, yscrollcommand=scrollbar.set, insertbackground=self.text_color)
        self.text_input.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_input.yview)
        self.placeholder = "请输入要转换为语音的文本..."
        self.text_input.insert("1.0", self.placeholder)
        self.text_input.config(fg="#999999")
        self.text_input.bind("<FocusIn>", self.on_focus_in)
        self.text_input.bind("<FocusOut>", self.on_focus_out)
        self.text_input.bind("<KeyRelease>", self.update_char_count)
        self.char_count_label = tk.Label(text_frame, text="字符数: 0", font=("微软雅黑", 9), fg="#999999", bg="#ffffff")
        self.char_count_label.pack(anchor="e", padx=15, pady=(0, 10))
        
        tk.Label(settings_frame, text="⚙️ 语音设置", font=("微软雅黑", 12, "bold"), fg=self.text_color, bg="#ffffff").pack(anchor="w", padx=15, pady=(15, 10))
        voice_container = tk.Frame(settings_frame, bg="#ffffff")
        voice_container.pack(fill="x", padx=15, pady=(0, 15))
        tk.Label(voice_container, text="选择声音:", font=("微软雅黑", 10), fg="#555555", bg="#ffffff").pack(side="left", padx=(0, 10))
        self.voice_var = tk.StringVar()
        voice_names = [f"{tag} - {info['name']}" for tag, info in self.tts.voices.items()]
        if voice_names: self.voice_var.set(voice_names[0])
        self.voice_dropdown = ttk.Combobox(voice_container, textvariable=self.voice_var, values=voice_names, font=("微软雅黑", 10), state='readonly')
        self.voice_dropdown.pack(side="left", fill="x", expand=True)
        
        button_inner_frame = tk.Frame(button_frame, bg="#ffffff")
        button_inner_frame.pack(pady=15)
        main_button_frame = tk.Frame(button_inner_frame, bg="#ffffff")
        main_button_frame.pack(pady=(0, 10))
        ttk.Button(main_button_frame, text="▶️ 生成并播放", style="Warning.Modern.TButton", command=self.generate_and_play).pack(side="left", padx=5)
        ttk.Button(main_button_frame, text="💾 生成并保存", style="Success.Modern.TButton", command=self.generate_audio).pack(side="left", padx=5)
        ttk.Button(main_button_frame, text="🔄 刷新声音", style="Primary.Modern.TButton", command=self.refresh_voices).pack(side="left", padx=5)
        control_button_frame = tk.Frame(button_inner_frame, bg="#ffffff")
        control_button_frame.pack()
        self.pause_btn = ttk.Button(control_button_frame, text="⏸️ 暂停", style="Secondary.Modern.TButton", command=self.toggle_pause, state="disabled")
        self.pause_btn.pack(side="left", padx=5)
        self.stop_btn = ttk.Button(control_button_frame, text="⏹️ 停止", style="Danger.Modern.TButton", command=self.stop_playback, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        status_indicator_frame = tk.Frame(control_button_frame, bg="#ffffff")
        status_indicator_frame.pack(side="left", padx=15, pady=(5,0))
        self.status_dot = tk.Canvas(status_indicator_frame, width=12, height=12, bg="#ffffff", highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 8))
        self.status_dot.create_oval(2, 2, 10, 10, fill="#999999", outline="#999999")
        self.playback_status = tk.Label(status_indicator_frame, text="未播放", font=("微软雅黑", 10), fg="#666666", bg="#ffffff")
        self.playback_status.pack(side="left")

    def on_focus_in(self, event):
        if self.text_input.get("1.0", "end-1c") == self.placeholder:
            self.text_input.delete("1.0", "end")
            self.text_input.config(fg=self.text_color)
            
    def on_focus_out(self, event):
        if not self.text_input.get("1.0", "end-1c"):
            self.text_input.insert("1.0", self.placeholder)
            self.text_input.config(fg="#999999")
            
    def update_char_count(self, event=None):
        text = self.text_input.get("1.0", "end-1c")
        count = 0 if text == self.placeholder else len(text)
        self.char_count_label.config(text=f"字符数: {count}")

    def update_status(self, icon, text, color):
        self.status_icon.config(text=icon, fg=color)
        self.status_label.config(text=text)

    def update_playback_status(self, text, color, dot_color):
        self.playback_status.config(text=text, fg=color)
        self.status_dot.delete("all")
        self.status_dot.create_oval(2, 2, 10, 10, fill=dot_color, outline=dot_color)

    def get_selected_voice_tag(self):
        selected = self.voice_var.get()
        return selected.split(' - ')[0] if selected else 'DeepSeek'
  
    def _generate_audio(self, callback):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text or text == self.placeholder:
            messagebox.showwarning("警告", "请输入要转换的文本！")
            return
        
        self.update_status("⏳", "正在生成音频...", self.warning_color)
        if callback == self.play_audio:
            self.update_playback_status("生成中...", self.warning_color, self.warning_color)
        self.root.update_idletasks()
        
        def generate_in_thread():
            try:
                audio_data = self.tts.get_audio(text, self.get_selected_voice_tag())
                self.root.after(0, lambda: callback(audio_data))
            except Exception as e:
                self.root.after(0, lambda: self.handle_error(f"生成音频时出错:\n\n{str(e)}"))
        
        threading.Thread(target=generate_in_thread, daemon=True).start()

    def generate_and_play(self):
        if not PYGAME_AVAILABLE:
            messagebox.showerror("错误", "Pygame 未安装或初始化失败，无法播放音频。\n\n请尝试运行: pip install pygame")
            return
        self._generate_audio(self.play_audio)

    def generate_audio(self):
        self._generate_audio(self.save_audio)
    
    def play_audio(self, audio_data):
        try:
            self.player.play(audio_data)
            file_size = len(audio_data) / 1024
            self.update_status("▶️", f"正在播放 ({file_size:.1f} KB)", self.success_color)
            self.update_playback_status("播放中", self.success_color, self.success_color)
            self.pause_btn.config(state="normal")
            self.stop_btn.config(state="normal")
        except Exception as e:
            self.handle_error(f"播放音频时出错:\n\n{str(e)}")

    def save_audio(self, audio_data):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                filetypes=[("MP3 音频文件", "*.mp3"), ("所有文件", "*.*")],
                initialfile=f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            )
            if filename:
                with open(filename, 'wb') as f: f.write(audio_data)
                file_size = len(audio_data) / 1024
                self.update_status("✓", f"音频已保存至 {os.path.basename(filename)} ({file_size:.1f} KB)", self.success_color)
                messagebox.showinfo("成功", f"音频已成功保存！\n\n文件: {os.path.basename(filename)}\n大小: {file_size:.1f} KB")
            else:
                self.update_status("❌", "已取消保存", "#666666")
        except Exception as e:
            self.handle_error(f"保存文件时出错:\n\n{str(e)}")

    def toggle_pause(self):
        if self.player.is_paused:
            self.player.resume()
            self.pause_btn.config(text="⏸️ 暂停")
            self.update_playback_status("播放中", self.success_color, self.success_color)
            self.update_status("▶️", "继续播放", self.success_color)
        else:
            self.player.pause()
            self.pause_btn.config(text="▶️ 继续")
            self.update_playback_status("已暂停", self.warning_color, self.warning_color)
            self.update_status("⏸️", "已暂停", self.warning_color)
  
    def stop_playback(self):
        self.player.stop()
        self.update_playback_status("已停止", "#666666", "#999999")
        self.update_status("⏹️", "播放已停止", "#666666")
        self.pause_btn.config(state="disabled", text="⏸️ 暂停")
        self.stop_btn.config(state="disabled")
  
    def check_playback_status(self):
        if self.player.is_playing and not self.player.is_paused and not self.player.is_busy():
            self.player.stop() # 清理临时文件
            self.update_playback_status("播放完成", self.success_color, self.success_color)
            self.update_status("✓", "播放完成", self.success_color)
            self.pause_btn.config(state="disabled", text="⏸️ 暂停")
            self.stop_btn.config(state="disabled")
        self.root.after(100, self.check_playback_status)
  
    def handle_error(self, message):
        self.update_status("❌", "操作失败", self.danger_color)
        self.update_playback_status("失败", self.danger_color, self.danger_color)
        messagebox.showerror("错误", message)
  
    def refresh_voices(self):
        self.update_status("⏳", "正在刷新声音列表...", self.warning_color)
        self.root.update_idletasks()
        
        def refresh_in_thread():
            try:
                self.tts.load_voices()
                voice_names = [f"{tag} - {info['name']}" for tag, info in self.tts.voices.items()]
                def update_in_main():
                    self.voice_dropdown['values'] = voice_names
                    if voice_names: self.voice_dropdown.set(voice_names[0])
                    self.update_status("✓", f"声音列表已刷新 (共 {len(self.tts.voices)} 个声音)", self.success_color)
                    messagebox.showinfo("成功", f"已加载 {len(self.tts.voices)} 个声音！")
                self.root.after(0, update_in_main)
            except Exception as e:
                self.root.after(0, lambda: self.handle_error(f"刷新声音列表时出错:\n\n{str(e)}"))
        
        threading.Thread(target=refresh_in_thread, daemon=True).start()

    def on_closing(self):
        self.player.stop()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TTSGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()