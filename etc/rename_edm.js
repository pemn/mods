//#!cscript

WScript.Echo("rename_edm");
var re1 = new RegExp(/(.+)\((\d+).*\.(.+)\.(.+)\)/i);

// WScript.Echo(re.exec('abc'));

var WshShell = WScript.CreateObject("WScript.Shell");
var WshSysEnv = WshShell.Environment("Process");

fso = WScript.CreateObject("Scripting.FileSystemObject");
fc = fso.GetFolder(".").SubFolders;
for(var objEnum = new Enumerator(fc); !objEnum.atEnd(); objEnum.moveNext()) {
  var name = objEnum.item().Name;
  // WScript.Echo(name);
  var m = re1.exec(name);
  if (m) {
    WScript.Echo("");
    WScript.Echo(m);
    var rename = m[4] + " - " + m[3] + m[2] + " - " + m[1]
    if (rename.substr(0,2) != "20") {
      rename = '20' + rename;
    }
    WScript.Echo(rename);
    objEnum.item().Move(rename);
  }
}
