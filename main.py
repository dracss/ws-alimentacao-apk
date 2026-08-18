# -*- coding: utf-8 -*-
"""
WS Alimentação — app Android (WebView).
Embute o app web (pasta webapp/) num WebView nativo. Assim a interface, as
telas e as exportações de PDF/Excel são exatamente as mesmas da versão web,
funcionando offline. Os arquivos exportados são capturados e salvos na pasta
Download do celular.
"""
import os, base64, re, time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.utils import platform

APP_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(APP_DIR, "webapp", "index.html")

# ---------------------------------------------------------------- Android ----
if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    from android.permissions import request_permissions, Permission

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Build = autoclass('android.os.Build$VERSION')
    Toast = autoclass('android.widget.Toast')
    String = autoclass('java.lang.String')

    def toast(msg):
        try:
            act = PythonActivity.mActivity
            act.runOnUiThread(_Runnable(lambda: Toast.makeText(
                act.getApplicationContext(), String(msg), Toast.LENGTH_LONG).show()))
        except Exception:
            pass

    class _Runnable(PythonJavaClass):
        __javainterfaces__ = ['java/lang/Runnable']
        __javacontext__ = 'app'
        def __init__(self, fn): super().__init__(); self.fn = fn
        @java_method('()V')
        def run(self):
            try: self.fn()
            except Exception: pass

    def salvar_download(url, content_disposition, mimetype):
        """Recebe um data-URL vindo do WebView, decodifica e salva em Download/."""
        try:
            # nome do arquivo (tenta o fragmento #fn=, senão gera um)
            nome = None
            m = re.search(r'#fn=([^&]+)', url or '')
            if m:
                from urllib.parse import unquote
                nome = unquote(m.group(1))
            # separa cabeçalho do base64
            head, _, b64 = (url or '').partition(',')
            if '#' in b64: b64 = b64.split('#', 1)[0]
            if 'base64' not in head:
                return
            data = base64.b64decode(b64)
            if not mimetype:
                mimetype = 'application/pdf' if 'pdf' in head else \
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            if not nome:
                ext = 'pdf' if 'pdf' in mimetype else ('xlsx' if 'sheet' in mimetype else 'json' if 'json' in mimetype else 'bin')
                nome = 'WS_%s.%s' % (time.strftime('%Y%m%d_%H%M%S'), ext)
            _gravar(nome, mimetype, data)
        except Exception as e:
            toast('Erro ao salvar: %s' % e)

    def _gravar(nome, mimetype, data):
        act = PythonActivity.mActivity
        resolver = act.getContentResolver()
        if Build.SDK_INT >= 29:
            ContentValues = autoclass('android.content.ContentValues')
            MediaStoreDownloads = autoclass('android.provider.MediaStore$Downloads')
            v = ContentValues()
            v.put('_display_name', nome)
            v.put('mime_type', mimetype)
            v.put('relative_path', 'Download/WS Alimentacao')
            uri = resolver.insert(MediaStoreDownloads.EXTERNAL_CONTENT_URI, v)
            out = resolver.openOutputStream(uri)
            out.write(bytearray(data)); out.flush(); out.close()
            toast('Salvo em Download/WS Alimentacao/%s' % nome)
            _abrir(uri, mimetype)
        else:
            Environment = autoclass('android.os.Environment')
            d = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            pasta = os.path.join(d.getAbsolutePath(), 'WS Alimentacao')
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, nome)
            with open(caminho, 'wb') as f:
                f.write(data)
            toast('Salvo em Download/WS Alimentacao/%s' % nome)

    def _abrir(uri, mimetype):
        try:
            Intent = autoclass('android.content.Intent')
            it = Intent(Intent.ACTION_VIEW)
            it.setDataAndType(uri, mimetype)
            it.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            it.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            PythonActivity.mActivity.startActivity(it)
        except Exception:
            pass

    class DownloadListener(PythonJavaClass):
        __javainterfaces__ = ['android/webkit/DownloadListener']
        __javacontext__ = 'app'
        @java_method('(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;J)V')
        def onDownloadStart(self, url, userAgent, contentDisposition, mimetype, contentLength):
            salvar_download(url, contentDisposition, mimetype)

    @run_on_ui_thread
    def criar_webview():
        act = PythonActivity.mActivity
        wv = WebView(act)
        s = wv.getSettings()
        s.setJavaScriptEnabled(True)
        s.setDomStorageEnabled(True)
        s.setDatabaseEnabled(True)
        s.setAllowFileAccess(True)
        try:
            s.setAllowFileAccessFromFileURLs(True)
            s.setAllowUniversalAccessFromFileURLs(True)
        except Exception:
            pass
        s.setBuiltInZoomControls(False)
        s.setUserAgentString(s.getUserAgentString() + ' WSAndroid')
        wv.setWebViewClient(WebViewClient())
        wv.setDownloadListener(DownloadListener())
        wv.loadUrl('file://' + INDEX)
        act.setContentView(wv)
        global _WEBVIEW
        _WEBVIEW = wv

    _WEBVIEW = None


class WSApp(App):
    def build(self):
        if platform == "android":
            try:
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                                     Permission.READ_EXTERNAL_STORAGE])
            except Exception:
                pass
            Clock.schedule_once(lambda *a: criar_webview(), 0.5)
            return Label(text="WS Alimentação\ncarregando...", halign="center")
        else:
            # Desktop: apenas informa como testar (o WebView é só no Android)
            return Label(text="WS Alimentação\n(Rode a versão web para testar no PC:\n"
                              "abra webapp/index.html no navegador)")


if __name__ == "__main__":
    WSApp().run()
