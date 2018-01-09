// bing.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "bing.h"
#include "io.h"
#include "stdio.h"
#include "fstream"
using namespace std;

#include "CvxText.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

void add_text(char* path, char* txtpath)
{
	IplImage *img = cvLoadImage(path);
	
	FILE *file = fopen(txtpath, "rb");
	if(file == NULL)
		return;
	char txt[512];
	fgets(txt, 512, file);
	DWORD len = MultiByteToWideChar(CP_ACP, 0, txt, -1, NULL, 0);
	wchar_t *wTxt = new wchar_t[len];
	MultiByteToWideChar(CP_ACP, 0, txt, -1, wTxt, len);

	CvxText text("msyh.ttf");
	float p = 0.5;
	text.setFont(NULL, NULL, NULL, &p);
	text.putText(img, txt, cvPoint(1400, 1000), CV_RGB(250,250,250));

	remove(path);
	cvSaveImage(path, img);
}

int main()
{
    char imgpath[] = "G:\\bingImage\\today.bmp";
	char txtpath[] = "G:\\bingImage\\today.txt";
    if(_access(imgpath,0) == -1)
        return FALSE;

	// add text
	add_text(imgpath, txtpath);

    wchar_t ptr_img[] = L"G:\\bingImage\\today.bmp";
    BOOL value = SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, ptr_img, SPIF_UPDATEINIFILE);
    return value;
}

//// 唯一的应用程序对象
//
//CWinApp theApp;
//
//using namespace std;
//
//int _tmain(int argc, TCHAR* argv[], TCHAR* envp[])
//{
//	int nRetCode = 0;
//
//	HMODULE hModule = ::GetModuleHandle(NULL);
//
//	if (hModule != NULL)
//	{
//		// 初始化 MFC 并在失败时显示错误
//		if (!AfxWinInit(hModule, NULL, ::GetCommandLine(), 0))
//		{
//			// TODO: 更改错误代码以符合您的需要
//			_tprintf(_T("错误: MFC 初始化失败\n"));
//			nRetCode = 1;
//		}
//		else
//		{
//			// TODO: 在此处为应用程序的行为编写代码。
//		}
//	}
//	else
//	{
//		// TODO: 更改错误代码以符合您的需要
//		_tprintf(_T("错误: GetModuleHandle 失败\n"));
//		nRetCode = 1;
//	}
//
//	return nRetCode;
//}
