//#!cscript

WScript.Echo("rename_edm");
var re1 = new RegExp(/(.+)\((.+)-(.+)-(.+)\)\.abc/i);

// WScript.Echo(re.exec('abc'));

var WshShell = WScript.CreateObject("WScript.Shell");
var WshSysEnv = WshShell.Environment("Process");

fso = WScript.CreateObject("Scripting.FileSystemObject");
fc = fso.GetFolder(".").Files;
for(var objEnum = new Enumerator(fc); !objEnum.atEnd(); objEnum.moveNext()) {
  var name = objEnum.item().Name;
  // WScript.Echo(name);
  var m = re1.exec(name);
  if (m) {
    WScript.Echo(m);
  }
}
