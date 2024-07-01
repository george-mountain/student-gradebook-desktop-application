[Setup]
AppName=Gradebook
AppVersion=1.0
DefaultDirName={commonpf}\Gradebook
DefaultGroupName=Gradebook
OutputDir=Output
OutputBaseFilename=GradebookSetup

; Define a custom variable for internal directory
[Code]
#define InternalDir "{app}\_internal"

[Files]
Source: "dist\Gradebook\Gradebook.exe"; DestDir: "{app}"
;Source: "dist\Gradebook\gradebook.db"; DestDir: "{app}"; Flags: ignoreversion; Permissions: everyone-full
Source: "dist\Gradebook\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs

; Additional files or directories to be installed can be added here

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"
Name: "desktopicon\uninstall"; Description: "Remove desktop icon during uninstallation"; GroupDescription: "Additional icons:"

[Icons]
Name: "{group}\Gradebook"; Filename: "{app}\Gradebook.exe"
Name: "{commondesktop}\Gradebook"; Filename: "{app}\Gradebook.exe"; Tasks: desktopicon

[UninstallDelete]
Type: filesandordirs; Name: "{commondesktop}\Gradebook.lnk"; Tasks: desktopicon\uninstall
