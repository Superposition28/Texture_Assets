Noesis Python Support
--
Noesis supports Python through a native binary module. In order to add format/functionality support, put .py scripts in this folder which implement a method named "registerNoesisTypes".

Take a look at __NPExample.txt for a complete model import+export sample module. You can rename the extension from .txt to .py if you want to be able import/export with it.

Alt+T,R is a quick shortcut for reloading plugins/Python scripts. You can also assign the reload plugins menu item to the shortcut of your choice, from the View->Interface->Customize dialog.

A trimmed down core 3.2.1 Python implementation is included. No modules (ctypes, sockets, etc.) are included - if you want support for them, you have to create a folder called "DLLs" under the Noesis folder and put them in it. DLLs not compiled for Python 3.2.1 may or may not work.

Your registerNoesisTypes method should register file handles, and define its own methods to act as file handlers. (see examples in existing scripts)

Noesis natively loads and makes the "noesis" and "rapi" modules available for import. However, the rapi module should only be accessed during file handler routines, because the entire underlying API is instanced.


The following methods are available for the "noesis" module:

	{"logOutput", Noesis_LogOutput, METH_VARARGS, "prints to log. (s)"}, //args=string
	{"logError", Noesis_LogOutput, METH_VARARGS, "logs error. (s)"}, //args=string
	{"logFlush", Noesis_LogFlush, METH_NOARGS, "flush log."}, //args=none
	{"logPopup", Noesis_LogPopup, METH_NOARGS, "pops up the debug log."}, //args=none
	{"allocBytes", Noesis_AllocByteArray, METH_VARARGS, "allocate byte array of predetermined size. (i)"}, //args=size
	{"allocType", Noesis_AllocType, METH_VARARGS, "allocate an internal noesis python type. (var) types: "
													//note that while stream objects will accept bytearrays, modifying the bytearray (resizing or reallocating) while the stream object is active can cause crashes
													"readStream (sO) "
													"writeStream (s) "
	}, //args=type name, others depending on type name
	{"deinterleaveBytes", Noesis_DeinterleaveBytes, METH_VARARGS, "pulls flat data out of an interleaved array. (Oiii)"}, //args=bytearray, offset in bytearray, size of element, stride between elements
	{"interleaveUniformBytes", Noesis_InterleaveUniformBytes, METH_VARARGS, "pulls interleaved data out of flat arrays of uniform size. (Oii)"}, //args=bytearray, size of element, number of elements
	{"swapEndianArray", Noesis_SwapEndianArray, METH_VARARGS, "returns the entire array endian-swapped at x bytes. (Oi|ii)"}, //args=source array, swap count, (optional) offset (in bytes, into array), stride
	{"validateListType", NoePyMath_ValidateListType, METH_VARARGS, "validates list contains only a given type. does not throw an exception if the list is empty or None. (OO)"}, //args=list, desired type
	{"validateListTypes", NoePyMath_ValidateListTypes, METH_VARARGS, "validates list contains only types. does not throw an exception if the list is empty or None. (OO)"}, //args=list, list of desired types
	{"doException", Noesis_DoException, METH_VARARGS, "custom routine to raise an exception. (s)"}, //args=string
	{"getMainPath", Noesis_GetMainPath, METH_NOARGS, "returns string to main executable file."}, //args=none
	{"getScenesPath", Noesis_GetScenesPath, METH_NOARGS, "returns path string to scenes directory."}, //args=none
	{"getPluginsPath", Noesis_GetPluginsPath, METH_NOARGS, "returns path string to plugins directory."}, //args=none
	{"getSelectedFile", Noesis_GetSelectedFile, METH_NOARGS, "returns path string to selected file."}, //args=none
	{"getSelectedDirectory", Noesis_GetSelectedDirectory, METH_NOARGS, "returns path string to selected directory."}, //args=none
	{"setSelectedDirectory", Noesis_SetSelectedDirectory, METH_VARARGS, "returns True if successful. (u)"}, //args=path
	{"getOpenPreviewFile", Noesis_GetOpenPreviewFile, METH_NOARGS, "returns path string to open preview file, or None if nothing is open."}, //args=none
	{"getAPIVersion", Noesis_GetAPIVersion, METH_NOARGS, "returns the api version."}, //args=none
	{"register", Noesis_Register, METH_VARARGS, "registers a file type. (ss)"}, //args=type name, type ext
	{"registerTool", Noesis_RegisterTool, METH_VARARGS, "registers a tool. returns a tool handle. (sO|s)"}, //args=tool name, tool method, tool help text (optional)
	{"registerCleanupFunction", Noesis_RegisterCleanupFunction, METH_VARARGS, "registers a cleanup function. (O)"}, //args=cleanup method
	{"disableFormatByDescription", Noesis_DisableFormatByDescription, METH_VARARGS, "disables a format by matching the full name string. (s)"}, //args=type name
	{"checkToolMenuItem", Noesis_CheckToolMenuItem, METH_VARARGS, "checks or unchecks a tool's menu item. (ii)"}, //args=tool handle, checked status
	{"setToolFlags", Noesis_SetToolFlags, METH_VARARGS, "sets a tool's flags. (ii)"}, //args=tool handle, flags
	{"getToolFlags", Noesis_GetToolFlags, METH_VARARGS, "returns a tool's flags. (i)"}, //args=tool handle
	{"setToolSubMenuName", Noesis_SetToolSubMenuName, METH_VARARGS, "sets a tool's submenu name. (is)"}, //args=tool handle, name
	{"setToolVisibleCallback", Noesis_SetToolVisibleCallback, METH_VARARGS, "sets visibility callback (is - toolHandle, selectedFile/None) for tool menu item. unlike most python callbacks, no special context cleanup is performed around this callback, so take care inside of it. (iO)"}, //args=tool handle, callback method

	{"registerVrMenuItem", Noesis_RegisterVrMenuItem, METH_VARARGS, "registers a vr menu item. returns the menu item index. (sO)"}, //args=tool name, tool method
	{"enterCustomVrMenuState", Noesis_EnterCustomVrMenuState, METH_VARARGS, "enter a custom menu. (OOO)"}, //args=item count method, item name method, item used method
	{"setCustomVrMenuItem", Noesis_SetCustomVrMenuItem, METH_VARARGS, "sets the custom menu selection index. (i)"}, //args=item index

	{"registerDebuggerDataHandler", Noesis_RegisterDebuggerDataHandler, METH_VARARGS, "registers a debugger data handler. returns a handle. (sO)"}, //args=title, callback method
	{"registerDebuggerTickCallback", Noesis_RegisterDebuggerTickCallback, METH_VARARGS, "registers a debugger callback. returns a handle. (O)"}, //args=callback method
	{"debuggerReadData", Noesis_DebuggerReadData, METH_VARARGS, "returns a bytearray or None upon failure. (QQ)"}, //args=address, size
	{"debuggerWriteData", Noesis_DebuggerWriteData, METH_VARARGS, "returns False upon failure. (QO)"}, //args=address, data

	{"openDataViewer", Noesis_OpenDataViewer, METH_NOARGS, "opens data viewer. returns true if successful."}, //args=none
	{"closeDataViewer", Noesis_CloseDataViewer, METH_NOARGS, "closes data viewer."}, //args=none
	{"getDataViewerSetting", Noesis_GetDataViewerSetting, METH_VARARGS, "returns value string, or None on failure. requires data viewer to be open. (s)"}, //args=value name
	{"setDataViewerSetting", Noesis_SetDataViewerSetting, METH_VARARGS, "sets value from string. requires data viewer to be open. (ss)"}, //args=value name, value

	{"addOption", Noesis_AddOption, METH_VARARGS, "adds an option for the registered type. (issi)"}, //args=handle, option name, option description, flags (e.g. OPTFLAG_WANTARG)
	{"optWasInvoked", Noesis_OptWasInvoked, METH_VARARGS, "returns non-0 if option has been invoked. (s)"}, //args=option name
	{"optGetArg", Noesis_OptGetArg, METH_VARARGS, "returns an argument string for the option. (s)"}, //args=option name

	{"userPrompt", Noesis_UserPrompt, METH_VARARGS, "displays a user input prompt. returns expected data type, or None on cancellation. (i|sssO)"}, //args=value type (a noesis.NOEUSERVAL_* constant), title string, prompt string, default value string, input validation handler
	{"messagePrompt", Noesis_MessagePrompt, METH_VARARGS, "displays a message box. (s)"}, //args=message string
	{"openFile", Noesis_OpenFile, METH_VARARGS, "opens a file in the main preview view. (s)"}, //args=file path
	{"openAndRemoveTempFile", Noesis_OpenAndRemoveTempFile, METH_VARARGS, "opens a file in the main preview view without browsing to it, and deletes it after opening. (s)"}, //args=file path
	{"fileIsLoadable", Noesis_FileIsLoadable, METH_VARARGS, "returns true if file is loadable. (s)"}, //args=file path
	{"isSupportedFileExtension", Noesis_IsSupportedFileExtension, METH_VARARGS, "returns true if extension is somewhere in the list of known ones. (s)"}, //args=file path

	{"loadImageRGBA", Noesis_LoadImageRGBA, METH_VARARGS, "loads the first image in a file and returns a NoeTexture. (s)"}, //args=file path
	{"saveImageRGBA", Noesis_SaveImageRGBA, METH_VARARGS, "saves a NoeTexture to a file. (sO)"}, //args=file path, texture object
	{"saveImageFromTexture", Noesis_SaveImageFromTexture, METH_VARARGS, "saves a NoeTexture to a file. (sO|O)"}, //args=file path, texture object, (optional) export options string

	{"instantiateModule", Noesis_InstantiateModule, METH_NOARGS, "returns a handle to a new module. make sure you use freeModule when you're done!"}, //args=none
	{"freeModule", Noesis_FreeModule, METH_VARARGS, "frees a module. (i)"}, //args=module handle
	{"setModuleRAPI", Noesis_SetModuleRAPI, METH_VARARGS, "sets a module's rapi interface to the active rapi. pass -1 to clear the active rapi. (i)"}, //args=module handle
	{"setPreviewModuleRAPI", Noesis_SetPreviewModuleRAPI, METH_NOARGS, "sets the active preview module's rapi interface to the active rapi. throws an exception if there is no active preview module."}, //args=none
	{"isPreviewModuleRAPIValid", Noesis_IsPreviewModuleRAPIValid, METH_NOARGS, "returns > 0 if preview module rapi is valid."}, //args=none
	{"storeCurrentRAPI", Noesis_StoreCurrentRAPI, METH_NOARGS, "stores a local handle to the current rapi instance, then invalidates the rapi instance."}, //args=none
	{"restoreCurrentRAPI", Noesis_RestoreCurrentRAPI, METH_NOARGS, "restores the rapi instance stored by storeCurrentRAPI."}, //args=none

	//push/pop preserves the local (python module) rapi instance like store/restore, but also preserves the internal (noesis) module state
	{"pushRAPIContext", Noesis_PushRAPIContext, METH_NOARGS, "pushes the current rapi module context."}, //args=none
	{"popRAPIContext", Noesis_PopRAPIContext, METH_NOARGS, "pops the current rapi module context."}, //args=none

	{"getCharSplineSet", Noesis_GetCharSplineSet, METH_VARARGS, "returns a NoeSplineSet for the given string character. (ord(c)) (i)"}, //args=character

	{"getWindowHandle", Noesis_GetWindowHandle, METH_NOARGS, "gets native platform window handle."}, //args=none

	{"getFormatExtensionFlags", Noesis_GetFormatExtensionFlags, METH_VARARGS, "returns a combination of noesis.NFORMATFLAG values for a file extension. (s)"}, //args=extension, including . at start

	{"usbOpenDevice", Noesis_UsbOpenDevice, METH_VARARGS, "returns a handle to the opened device. (uu)"}, //args=device interface GUID, device class GUID
	{"usbCloseDevice", Noesis_UsbCloseDevice, METH_VARARGS, "closes a handle opened by usbOpenDevice. (i)"}, //args=device handle
	{"usbSetAltInterface", Noesis_UsbSetAltInterface, METH_VARARGS, "sets an alternate interface. (ii)"}, //args=device handle, alt interface index
	{"usbGetEndpointCount", Noesis_UsbGetEndpointCount, METH_VARARGS, "get endpoint count for current interface. (i)"}, //args=device handle
	{"usbGetEndpointInfo", Noesis_UsbGetEndpointInfo, METH_VARARGS, "gets a tuple of parameters for specified ep in current interface. (ii)"}, //args=device handle, endpoint index
	{"usbWriteEndpoint", Noesis_UsbWriteEndpoint, METH_VARARGS, "writes data to endpoint. (iiO)"}, //args=device handle, endpoint index, data
	{"usbWriteEndpointId", Noesis_UsbWriteEndpointId, METH_VARARGS, "writes data to endpoint. (iiO)"}, //args=device handle, endpoint id, data
	{"usbReadEndpoint", Noesis_UsbReadEndpoint, METH_VARARGS, "reads data from endpoint. (iii)"}, //args=device handle, endpoint index, size
	{"usbReadEndpointId", Noesis_UsbReadEndpointId, METH_VARARGS, "reads data from endpoint. (iii)"}, //args=device handle, endpoint id, size
	{"usbControlTransfer", Noesis_UsbControlTransfer, METH_VARARGS, "reads data from endpoint. (iOiiii)"}, //args=device handle, data, request type, request, index, value
	{"usbSetEndpointTimeout", Noesis_UsbSetEndpointTimeout, METH_VARARGS, "sets timeout on endpoint. (iii)"}, //args=device handle, endpoint index, timeout value
	{"usbSetEndpointTimeoutId", Noesis_UsbSetEndpointTimeoutId, METH_VARARGS, "sets timeout on endpoint. (iii)"}, //args=device handle, endpoint id, timeout value

	{"comGetPortPaths", Noesis_ComGetPortPaths, METH_NOARGS, "returns a list of (com index, com path) tuples."}, //args=none
	{"comOpenPort", Noesis_ComOpenPort, METH_VARARGS, "returns a handle to the open port. (i)"}, //args=port index
	{"comClosePort", Noesis_ComClosePort, METH_VARARGS, "closes an open port. (i)"}, //args=port handle
	{"comGetInfo", Noesis_ComGetInfo, METH_VARARGS, "returns tuple of (baud rate, byte size, parity, stop bits). (i)"}, //args=port handle
	{"comSetInfo", Noesis_ComSetInfo, METH_VARARGS, "sets port info. (iiiii)"}, //args=port handle, baud rate, byte size, parity, stop bits
	{"comGetTimeouts", Noesis_ComGetTimeouts, METH_VARARGS, "returns tuple of (read interval timeout, read timeout multiplier, read timeout constant, write timeout multiplier, write timeout constant). (i)"}, //args=port handle
	{"comSetTimeouts", Noesis_ComSetTimeouts, METH_VARARGS, "sets port timeouts. (iiiiii)"}, //args=port handle, read interval timeout, read timeout multiplier, read timeout constant, write timeout multiplier, write timeout constant
	{"comRead", Noesis_ComRead, METH_VARARGS, "returns bytearray of data read. (ii)"}, //args=port handle, max number of bytes to read
	{"comWrite", Noesis_ComWrite, METH_VARARGS, "returns number of bytes written. (iO)"}, //args=port handle, data to write

	{"desktopCapStart", Noesis_DesktopCapStart, METH_VARARGS, "returns True on success. (iiii)"}, //args=mode (0=raw,1=jpeg,2=png), delay (milliseconds), encoding quality, encoding shift
	{"desktopCapEnd", Noesis_DesktopCapEnd, METH_NOARGS, "should only be called when desktopCapStart returns True."}, //args=none
	{"desktopCapGetOldestBuffer", Noesis_DesktopGetOldestBuffer, METH_NOARGS, "returns tuple of (buffer, width, height), or None upon failure."}, //args=none
	{"desktopCapClearOldestBuffer", Noesis_DesktopClearOldestBuffer, METH_NOARGS, "internally frees the oldest buffer in the queue."}, //args=none
	{"desktopCapClearOldestBufferIfAvailable", Noesis_DesktopClearOldestBufferIfAvailable, METH_VARARGS, "internally frees the oldest buffer in the queue, if more than given count are available. (i)"}, //args=minimum count
	{"desktopCapAvailableBufferCount", Noesis_DesktopAvailableBufferCount, METH_NOARGS, "returns the number of available capture buffers."}, //args=none

	{"nativeYield", Noesis_NativeYield, METH_NOARGS, "yields the native thread."}, //args=none

	{"jaguarRISCDisassemble", Noesis_JaguarRISCDisassemble, METH_VARARGS, "returns tuple of (opSize, text). (Oi)"}, //args=data, risc type (0=gpu)
	{"jaguarM68KDisassemble", Noesis_JaguarM68KDisassemble, METH_VARARGS, "returns tuple of (opSize, text). (Oi)"}, //args=data, destination address

	//typecheck handler should be defined as def fmtCheckType(data), where data is a PyByteArray
	//should return 0 on fail (is not the format) or 1 on success (is the format)
	{"setHandlerTypeCheck", Noesis_SetHandlerTypeCheck, METH_VARARGS, "sets the type check handler. (iO)"}, //args=handle, function

	//loadmodel handler should be defined as def fmtLoadModel(data, mdlList), where data is a PyByteArray and mdlList is an empty list that should be filled with NoeModel objects
	//should return 0 on fail or 1 on success
	{"setHandlerLoadModel", Noesis_SetHandlerLoadModel, METH_VARARGS, "sets the model load handler. (iO)"}, //args=handle, function

	//writemodel handler should be defined as def fmtWriteModel(mdl, bsOut), where mdl is a NoeModel (the model being exported) and bsOut is a NoeBitStream that should have the resulting model binary written into it
	//should return 0 on fail or 1 on success
	{"setHandlerWriteModel", Noesis_SetHandlerWriteModel, METH_VARARGS, "sets the model write handler. (iO)"}, //args=handle, function

	//writeanim handler should be defined as def fmtWriteAnim(anims, bsOut), where anims is a list of NoeAnim and bsOut is a NoeBitStream that should have the resulting anim binary written into it
	//should return 0 on fail (or in the event that the NoeBitStream should not be written to disk) or 1 on success
	{"setHandlerWriteAnim", Noesis_SetHandlerWriteAnim, METH_VARARGS, "sets the animation write handler. (iO)"}, //args=handle, function

	//loadrgba handler should be defined as def fmtLoadRGBA(data, texList), where data is a PyByteArray and texList is an empty list that should be filled with NoeTexture objects
	//should return 0 on fail or 1 on success
	{"setHandlerLoadRGBA", Noesis_SetHandlerLoadRGBA, METH_VARARGS, "sets the image load handler. (iO)"}, //args=handle, function

	//writergba handler should be defined as def fmtWriteRGBA(data, width, height, bsOut), where data is a PyByteArray of 32bpp rgba, width/height are the image dimensions, and bsOut is a NoeBitStream that should have the resulting binary written into it
	//should return 0 on fail or 1 on success
	{"setHandlerWriteRGBA", Noesis_SetHandlerWriteRGBA, METH_VARARGS, "sets the image write handler. (iO)"}, //args=handle, function

	//extractarc handler should be defined as def fmtExtractArc(fileName, fileLen, justChecking), where fileName is a string (you should handle opening the file yourself in the handler), fileLen is an int/long, and justChecking (means you should return 1 as soon as you have determined the validity of the type) is an int
	//should return 0 on fail or 1 on success
	{"setHandlerExtractArc", Noesis_SetHandlerExtractArc, METH_VARARGS, "sets the archive handler. (iO)"}, //args=handle, function

	//when this format is the main export target, the provided string will be run through the advanced options parser
	{"setTypeExportOptions", Noesis_SetTypeExportOptions, METH_VARARGS, "sets the type's export options. (is)"}, //args=handle, function

	//specifies shared model flags to be used when exporting a model for this format in python
	{"setTypeSharedModelFlags", Noesis_SetTypeSharedModelFlags, METH_VARARGS, "sets the type's shared model flags. (NMSHAREDFL_*) (ii)"}, //args=handle, flags

	{"pumpModalStatus", Noesis_PumpModalStatus, METH_VARARGS, "pumps the modal status dialog. (sf)"}, //args=message, duration (in seconds) until dialog clears
	{"clearModalStatus", Noesis_ClearModalStatus, METH_NOARGS, "clears the modal status dialog if it's displayed.)"}, //args=none

	{"getResourceHandle", Noesis_GetResourceHandle, METH_VARARGS, "returns a resource handle. (i)"}, //args=resource index

	//math functions
	{"nextPow2", NoePyMath_NextPow2, METH_VARARGS, "returns next power of 2 value. (i)"}, //args=int
	{"getFloat16", NoePyMath_GetFloat16, METH_VARARGS, "returns float from half-float. (H)"}, //args=ushort
	{"encodeFloat16", NoePyMath_EncodeFloat16, METH_VARARGS, "returns half-float from float. (f)"}, //args=float
	{"getMFFP", NoePyMath_GetMFFP, METH_VARARGS, "returns float from motorola fast floating point format. (I)"}, //args=uint
	{"encodeMFFP", NoePyMath_EncodeMFFP, METH_VARARGS, "returns motorola FFP from float. (f)"}, //args=float
	{"getArbitraryFloat", NoePyMath_GetArbitraryFloat, METH_VARARGS, "decodes arbitrary float. (IIII)"}, //args=uint, frac bits, exp bits, sign bits
	{"encodeArbitraryFloat", NoePyMath_EncodeArbitraryFloat, METH_VARARGS, "encodes arbitrary float. (fIII)"}, //args=float, frac bits, exp bits, sign bits
	{"signedBits", NoePyMath_SignedBits, METH_VARARGS, "returns signed interpretation of unsigned value. (KK)"}, //args=value, bits
	{"transformBits", NoePyMath_TransformBits, METH_VARARGS, "returns value transformed using a bytearray matrix/LUT. (KO)"}, //args=value, bytearray matrix
	{"transformBitsArray", NoePyMath_TransformBitsArray, METH_VARARGS, "as above, performing transforms on an input bytearray. (OIO)"}, //args=bytearray input, element size in bytes, bytearray matrix
	{"transformBitsInverse", NoePyMath_TransformBitsInverse, METH_VARARGS, "returns value transformed using a bytearray matrix/LUT. (KO)"}, //args=value, bytearray matrix
	{"transformBitsInverseArray", NoePyMath_TransformBitsInverseArray, METH_VARARGS, "as above, performing transforms on an input bytearray. (OIO)"}, //args=bytearray input, element size in bytes, bytearray matrix
	{"morton2D", NoePyMath_Morton2D, METH_VARARGS, "returns morton index from x,y coordinates. (ii)"}, //args=x, y
	//sorry, i just came in here to add a function and saw that for some reason i kept using "lerp" to describe any kind of interpolation in here, so these functions have terrible/comical names.
	//being the monster that i was, it's possible that i actually thought this was funny at the time, or i may have been drinking.
	{"constLerp", NoePyMath_ConstLerp, METH_VARARGS, "constant interpolation. (fff)"}, //args=float 1, float 2, fraction
	{"linLerp", NoePyMath_LinLerp, METH_VARARGS, "linear interpolation. (fff)"}, //args=float 1, float 2, fraction
	{"bilinLerp", NoePyMath_BilinLerp, METH_VARARGS, "bilinear interpolation. (ffffff)"}, //args=x, y, z, w, frac1, frac2
	{"triLerp", NoePyMath_TriLerp, METH_VARARGS, "trilinear interpolation. (ffffff)"}, //args=x, y, z, frac1, frac2, frac3
	{"cubicLerp", NoePyMath_CubicLerp, METH_VARARGS, "cubic interpolation. (fffff)"}, //args=y0, y1, y2, y3, frac
	{"hermiteLerp", NoePyMath_HermiteLerp, METH_VARARGS, "cubic hermite interpolation. (fffffff)"}, //args=y0, y1, y2, y3, frac, tension, bias
	{"bezier3D", NoePyMath_Bezier3D, METH_VARARGS, "returns point on bezier spline. (Of)"}, //args=list of points, fraction
	{"bezierTangent3D", NoePyMath_BezierTangent3D, METH_VARARGS, "returns tangent on a bezier spline. (Of)"}, //args=list of 4 points, fraction
	{"cubicBezier3D", NoePyMath_CubicBezier3D, METH_VARARGS, "returns point on cubic bezier spline. (Of)"}, //args=list of 4 points, fraction
	{"planeFromPoints", NoePyMath_PlaneFromPoints, METH_VARARGS, "returns a plane(NoeVec4) from 3 points. (OOO)"}, //args=NoeVec3, NoeVec3, NoeVec3
	{"countBits", NoePyMath_CountBits, METH_VARARGS, "returns number of bits set. (I)"}, //args=int
	{"lerpSamples", NoePyMath_LerpSamples, METH_VARARGS, "returns interpolated tuple of values. (OI)"}, //args=tuple of (index,value) pairs, sample count
	{"nybbleSwap", NoePyMath_NybbleSwap, METH_VARARGS, "swap nybble order in bytearray. (O)"}, //args=bytes
	{"log2", NoePyMath_Log2, METH_VARARGS, "returns base 2 logarithm. (O)"}, //args=bytes

Various other math and streaming functions are also exposed, but it's best to use the Noe* types (see inc_noesis.py) instead of accessing those methods directly.

The following constants are also exposed:

	PYNOECONSTN(NOESIS_PLUGIN_VERSION),
	PYNOECONSTN(NOESIS_PLUGINAPI_VERSION),
	PYNOECONSTN(MAX_NOESIS_PATH),

	PYNOECONSTN(NOESISTEX_UNKNOWN),
	PYNOECONSTN(NOESISTEX_RGBA32),
	PYNOECONSTN(NOESISTEX_RGB24),
	PYNOECONSTN(NOESISTEX_DXT1),
	PYNOECONSTN(NOESISTEX_DXT3),
	PYNOECONSTN(NOESISTEX_DXT5),

	PYNOECONSTN(FOURCC_DXT1),
	PYNOECONSTN(FOURCC_DXT3),
	PYNOECONSTN(FOURCC_DXT5),
	PYNOECONSTN(FOURCC_DXT1NORMAL),
	PYNOECONSTN(FOURCC_ATI1),
	PYNOECONSTN(FOURCC_ATI2),
	PYNOECONSTN(FOURCC_DX10),
	PYNOECONSTN(FOURCC_BC1),
	PYNOECONSTN(FOURCC_BC2),
	PYNOECONSTN(FOURCC_BC3),
	PYNOECONSTN(FOURCC_BC4),
	PYNOECONSTN(FOURCC_BC5),
	PYNOECONSTN(FOURCC_BC6H),
	PYNOECONSTN(FOURCC_BC6S),
	PYNOECONSTN(FOURCC_BC7),

	PYNOECONSTN(NOEFSMODE_READBINARY),
	PYNOECONSTN(NOEFSMODE_WRITEBINARY),
	PYNOECONSTN(NOEFSMODE_READWRITEBINARY),

	PYNOECONSTN(NTOOLFLAG_CONTEXTITEM),
	PYNOECONSTN(NTOOLFLAG_USERBITS),

	PYNOECONSTN(NFORMATFLAG_ARCREAD),
	PYNOECONSTN(NFORMATFLAG_IMGREAD),
	PYNOECONSTN(NFORMATFLAG_IMGWRITE),
	PYNOECONSTN(NFORMATFLAG_MODELREAD),
	PYNOECONSTN(NFORMATFLAG_MODELWRITE),
	PYNOECONSTN(NFORMATFLAG_ANIMWRITE),

	PYNOECONSTN(NTEXFLAG_WRAP_REPEAT),
	PYNOECONSTN(NTEXFLAG_ISNORMALMAP),
	PYNOECONSTN(NTEXFLAG_SEGMENTED),
	PYNOECONSTN(NTEXFLAG_STEREO),
	PYNOECONSTN(NTEXFLAG_STEREO_SWAP),
	PYNOECONSTN(NTEXFLAG_FILTER_NEAREST),
	PYNOECONSTN(NTEXFLAG_WRAP_CLAMP),
	PYNOECONSTN(NTEXFLAG_PREVIEWLOAD),
	PYNOECONSTN(NTEXFLAG_CUBEMAP),
	PYNOECONSTN(NTEXFLAG_ISLINEAR),
	PYNOECONSTN(NTEXFLAG_HDRISLINEAR),
	PYNOECONSTN(NTEXFLAG_WANTSEAMLESS),
	PYNOECONSTN(NTEXFLAG_WRAP_MIRROR_REPEAT),
	PYNOECONSTN(NTEXFLAG_WRAP_MIRROR_CLAMP),
	PYNOECONSTN(NTEXFLAG_WRAP_SEP_ST),
	PYNOECONSTN(NTEXFLAG_WRAP_T_REPEAT),
	PYNOECONSTN(NTEXFLAG_WRAP_T_CLAMP),
	PYNOECONSTN(NTEXFLAG_WRAP_T_MIRROR_REPEAT),
	PYNOECONSTN(NTEXFLAG_WRAP_T_MIRROR_CLAMP),

	PYNOECONSTN(NMATFLAG_NMAPSWAPRA),
	PYNOECONSTN(NMATFLAG_TWOSIDED),
	PYNOECONSTN(NMATFLAG_PREVIEWLOAD),
	PYNOECONSTN(NMATFLAG_USELMUVS),
	PYNOECONSTN(NMATFLAG_BLENDEDNORMALS),
	PYNOECONSTN(NMATFLAG_KAJIYAKAY),
	PYNOECONSTN(NMATFLAG_SORT01),
	PYNOECONSTN(NMATFLAG_GAMMACORRECT),
	PYNOECONSTN(NMATFLAG_VCOLORSUBTRACT),
	PYNOECONSTN(NMATFLAG_PBR_SPEC),
	PYNOECONSTN(NMATFLAG_PBR_METAL),
	PYNOECONSTN(NMATFLAG_NORMALMAP_FLIPY),
	PYNOECONSTN(NMATFLAG_NORMALMAP_NODERZ),
	PYNOECONSTN(NMATFLAG_PBR_SPEC_IR_RG),
	PYNOECONSTN(NMATFLAG_ENV_FLIP),
	PYNOECONSTN(NMATFLAG_PBR_ALBEDOENERGYCON),
	PYNOECONSTN(NMATFLAG_PBR_COMPENERGYCON),
	PYNOECONSTN(NMATFLAG_SPRITE_FACINGXY),
	PYNOECONSTN(NMATFLAG_NORMAL_UV1),
	PYNOECONSTN(NMATFLAG_SPEC_UV1),
	PYNOECONSTN(NMATFLAG_BASICBLEND),
	PYNOECONSTN(NMATFLAG_FORCESELFSORT),
	PYNOECONSTN(NMATFLAG_PBR_ROUGHNESS_NRMALPHA),
	PYNOECONSTN(NMATFLAG_DIFFUSE_UV1),
	PYNOECONSTN(NMATFLAG_UV1_ANY),

	PYNOECONSTN(NMATFLAG2_LMMASK),
	PYNOECONSTN(NMATFLAG2_VCOLORMATDIFFUSE),
	PYNOECONSTN(NMATFLAG2_PREFERPPL),
	PYNOECONSTN(NMATFLAG2_SPEC_IS_GAMMASPACE),
	PYNOECONSTN(NMATFLAG2_OCCL_UV1),
	PYNOECONSTN(NMATFLAG2_OCCL_ISLM),
	PYNOECONSTN(NMATFLAG2_OCCL_BLUE),
	PYNOECONSTN(NMATFLAG2_ENV_FLIP_Y),
	PYNOECONSTN(NMATFLAG2_UV1_ANY),
	PYNOECONSTN(NMATFLAG2_UV2_ANY),
	PYNOECONSTN(NMATFLAG2_DECAL),
	PYNOECONSTN(NMATFLAG2_CAVITY_PBR_BLUE),
	PYNOECONSTN(NMATFLAG2_OPACITY_UV1),
	PYNOECONSTN(NMATFLAG2_OPACITY_UV2),

	PYNOECONSTN(NSEQFLAG_NONLOOPING),
	PYNOECONSTN(NSEQFLAG_REVERSE),

	PYNOECONSTN(NANIMFLAG_FORCENAMEMATCH),
	PYNOECONSTN(NANIMFLAG_INVALIDHIERARCHY),

	PYNOECONSTN(RPGEO_NONE),
	PYNOECONSTN(RPGEO_POINTS),
	PYNOECONSTN(RPGEO_TRIANGLE),
	PYNOECONSTN(RPGEO_TRIANGLE_STRIP),
	PYNOECONSTN(RPGEO_QUAD), //ABC_DCB
	PYNOECONSTN(RPGEO_POLYGON),
	PYNOECONSTN(RPGEO_TRIANGLE_FAN),
	PYNOECONSTN(RPGEO_QUAD_STRIP),
	PYNOECONSTN(RPGEO_TRIANGLE_STRIP_FLIPPED),
	PYNOECONSTN(NUM_RPGEO_TYPES),
	PYNOECONSTN(RPGEO_QUAD_ABC_BCD),
	PYNOECONSTN(RPGEO_QUAD_ABC_ACD),
	PYNOECONSTN(RPGEO_QUAD_ABC_DCA),

	PYNOECONSTN(RPGEODATA_FLOAT),
	PYNOECONSTN(RPGEODATA_INT),
	PYNOECONSTN(RPGEODATA_UINT),
	PYNOECONSTN(RPGEODATA_SHORT),
	PYNOECONSTN(RPGEODATA_USHORT),
	PYNOECONSTN(RPGEODATA_HALFFLOAT),
	PYNOECONSTN(RPGEODATA_DOUBLE),
	PYNOECONSTN(RPGEODATA_BYTE),
	PYNOECONSTN(RPGEODATA_UBYTE),
	PYNOECONSTN(NUM_RPGEO_DATATYPES),

	PYNOECONSTN(NMSHAREDFL_WANTNEIGHBORS),
	PYNOECONSTN(NMSHAREDFL_WANTGLOBALARRAY),
	PYNOECONSTN(NMSHAREDFL_WANTTANGENTS),
	PYNOECONSTN(NMSHAREDFL_FLATWEIGHTS),
	PYNOECONSTN(NMSHAREDFL_FLATWEIGHTS_FORCE4),
	PYNOECONSTN(NMSHAREDFL_REVERSEWINDING),
	PYNOECONSTN(NMSHAREDFL_WANTTANGENTS4),
	PYNOECONSTN(NMSHAREDFL_WANTTANGENTS4R),
	PYNOECONSTN(NMSHAREDFL_UNIQUEVERTS),
	PYNOECONSTN(NMSHAREDFL_BONEPALETTE),
	PYNOECONSTN(NMSHAREDFL_NO_CREATE_UVS),

	PYNOECONSTN(SHAREDSTRIP_LIST),
	PYNOECONSTN(SHAREDSTRIP_STRIP),

	PYNOECONSTN(RPGOPT_BIGENDIAN),
	PYNOECONSTN(RPGOPT_TRIWINDBACKWARD),
	PYNOECONSTN(RPGOPT_TANMATROTATE),
	PYNOECONSTN(RPGOPT_DERIVEBONEORIS),
	PYNOECONSTN(RPGOPT_FILLINWEIGHTS),
	PYNOECONSTN(RPGOPT_SWAPHANDEDNESS),
	PYNOECONSTN(RPGOPT_UNSAFE),
	PYNOECONSTN(RPGOPT_MORPH_RELATIVEPOSITIONS),
	PYNOECONSTN(RPGOPT_MORPH_RELATIVENORMALS),
	PYNOECONSTN(RPGOPT_SNAPTANGENTW),
	PYNOECONSTN(RPGOPT_GEOTWOSIDEDPRV),
	PYNOECONSTN(RPGOPT_SANITIZEWEIGHTS),
	PYNOECONSTN(RPGOPT_FIXTRIWINDINGS),
	PYNOECONSTN(RPGOPT_NOINDEXLIMIT),

	PYNOECONSTN(RPGVUFLAG_PERINSTANCE),
	PYNOECONSTN(RPGVUFLAG_NOREUSE),

	PYNOECONSTN(OPTFLAG_WANTARG),

	PYNOECONSTN(DECODEFLAG_PS2SHIFT),

	PYNOECONSTN(BLITFLAG_ALPHABLEND),
	PYNOECONSTN(BLITFLAG_ALLOWCLIP),
	PYNOECONSTN(BLITFLAG_ALPHATEST),

	PYNOECONSTN(NOEUSERVAL_NONE),
	PYNOECONSTN(NOEUSERVAL_STRING),
	PYNOECONSTN(NOEUSERVAL_FLOAT),
	PYNOECONSTN(NOEUSERVAL_INT),
	PYNOECONSTN(NOEUSERVAL_BOOL),
	PYNOECONSTN(NOEUSERVAL_FILEPATH),
	PYNOECONSTN(NOEUSERVAL_FOLDERPATH),
	PYNOECONSTN(NOEUSERVAL_SAVEFILEPATH),

	PYNOECONSTN(NOEBLEND_NONE),
	PYNOECONSTN(NOEBLEND_ZERO),
	PYNOECONSTN(NOEBLEND_ONE),
	PYNOECONSTN(NOEBLEND_SRC_COLOR),
	PYNOECONSTN(NOEBLEND_ONE_MINUS_SRC_COLOR),
	PYNOECONSTN(NOEBLEND_SRC_ALPHA),
	PYNOECONSTN(NOEBLEND_ONE_MINUS_SRC_ALPHA),
	PYNOECONSTN(NOEBLEND_DST_ALPHA),
	PYNOECONSTN(NOEBLEND_ONE_MINUS_DST_ALPHA),
	PYNOECONSTN(NOEBLEND_DST_COLOR),
	PYNOECONSTN(NOEBLEND_ONE_MINUS_DST_COLOR),
	PYNOECONSTN(NOEBLEND_SRC_ALPHA_SATURATE),
	PYNOECONSTN(NUM_NOE_BLENDS),

	PYNOECONSTN(NOESPLINEFLAG_CLOSED),

	PYNOECONSTF(g_flPI),
	PYNOECONSTF(g_flDegToRad),
	PYNOECONSTF(g_flRadToDeg),

	PYNOECONSTN(PS2_VIFCODE_NOP),
	PYNOECONSTN(PS2_VIFCODE_STCYCL),
	PYNOECONSTN(PS2_VIFCODE_OFFSET),
	PYNOECONSTN(PS2_VIFCODE_BASE),
	PYNOECONSTN(PS2_VIFCODE_ITOP),
	PYNOECONSTN(PS2_VIFCODE_STMOD),
	PYNOECONSTN(PS2_VIFCODE_MSKPATH3),
	PYNOECONSTN(PS2_VIFCODE_MARK),
	PYNOECONSTN(PS2_VIFCODE_FLUSHE),
	PYNOECONSTN(PS2_VIFCODE_FLUSH),
	PYNOECONSTN(PS2_VIFCODE_FLUSHA),
	PYNOECONSTN(PS2_VIFCODE_MSCAL),
	PYNOECONSTN(PS2_VIFCODE_MSCNT),
	PYNOECONSTN(PS2_VIFCODE_MSCALF),
	PYNOECONSTN(PS2_VIFCODE_STMASK),
	PYNOECONSTN(PS2_VIFCODE_STROW),
	PYNOECONSTN(PS2_VIFCODE_STCOL),
	PYNOECONSTN(PS2_VIFCODE_MPG),
	PYNOECONSTN(PS2_VIFCODE_DIRECT),
	PYNOECONSTN(PS2_VIFCODE_DIRECTHL),

	PYNOECONSTN(BONEFLAG_ORTHOLERP),
	PYNOECONSTN(BONEFLAG_DIRECTLERP),
	PYNOECONSTN(BONEFLAG_NOLERP),
	PYNOECONSTN(BONEFLAG_DECOMPLERP),

	PYNOECONSTN(BITSTREAMFL_BIGENDIAN),
	PYNOECONSTN(BITSTREAMFL_DESCENDINGBITS),
	PYNOECONSTN(BITSTREAMFL_USERFLAG1),
	PYNOECONSTN(BITSTREAMFL_USERFLAG2),
	PYNOECONSTN(BITSTREAMFL_USERFLAG3),
	PYNOECONSTN(BITSTREAMFL_USERFLAG4),
	PYNOECONSTN(BITSTREAMFL_USERFLAG5),
	PYNOECONSTN(BITSTREAMFL_USERFLAG6),
	PYNOECONSTN(BITSTREAMFL_USERFLAG7),
	PYNOECONSTN(BITSTREAMFL_USERFLAG8),

	PYNOECONSTN(NOEKF_ROTATION_QUATERNION_4),
	PYNOECONSTN(NOEKF_ROTATION_EULER_XYZ_3),
	PYNOECONSTN(NOEKF_ROTATION_EULER_SINGLE),
	PYNOECONSTN(NOEKF_ROTATION_MATRIX_33),
	PYNOECONSTN(NUM_NOEKF_ROTATION_TYPES),
	PYNOECONSTN(NOEKF_TRANSLATION_VECTOR_3),
	PYNOECONSTN(NOEKF_TRANSLATION_SINGLE),
	PYNOECONSTN(NUM_NOEKF_TRANSLATION_TYPES),
	PYNOECONSTN(NOEKF_SCALE_SCALAR_1),
	PYNOECONSTN(NOEKF_SCALE_SINGLE),
	PYNOECONSTN(NOEKF_SCALE_VECTOR_3),
	PYNOECONSTN(NOEKF_SCALE_TRANSPOSED_VECTOR_3),
	PYNOECONSTN(NUM_NOEKF_SCALE_TYPES),
	PYNOECONSTN(NOEKF_INTERPOLATE_LINEAR),
	PYNOECONSTN(NOEKF_INTERPOLATE_NEAREST),
	PYNOECONSTN(NOEKF_INTERPOLATE_CATMULLROM),
	PYNOECONSTN(NOEKF_INTERPOLATE_TCB),
	PYNOECONSTN(NOEKF_INTERPOLATE_HERMITE),
	PYNOECONSTN(NOEKF_INTERPOLATE_BEZIER),
	PYNOECONSTN(NOEKF_INTERPOLATE_BEZIER_R),
	PYNOECONSTN(NUM_NOEKF_INTERPOLATION_TYPES),

	PYNOECONSTN(KFDFLAG_COMPONENT_MASK),
	PYNOECONSTN(KFDFLAG_EASE),
	PYNOECONSTN(KFDFLAG_WRAP_TO_LAST),
	PYNOECONSTN(KFDFLAG_WRAP_TO_FIRST),
	PYNOECONSTN(KFDFLAG_SMOOTHTANGENTS),

	PYNOECONSTN(KFBONEFLAG_MODELSPACE),
	PYNOECONSTN(KFBONEFLAG_ADDITIVE),
	PYNOECONSTN(KFBONEFLAG_ADDITIVE_TP),
	PYNOECONSTN(KFBONEFLAG_NLERP),
	PYNOECONSTN(KFBONEFLAG_NLERP_TP),

	PYNOECONSTN(KFANIMFLAG_SEPARATETS),
	PYNOECONSTN(KFANIMFLAG_TRANSPOSESCALE),
	PYNOECONSTN(KFANIMFLAG_USEBONETIMES),
	PYNOECONSTN(KFANIMFLAG_PLUSONE),
	PYNOECONSTN(KFANIMFLAG_ROUNDUP),

	PYNOECONSTN(PVRTC_DECODE_PVRTC2),
	PYNOECONSTN(PVRTC_DECODE_LINEARORDER),
	PYNOECONSTN(PVRTC_DECODE_BICUBIC),
	PYNOECONSTN(PVRTC_DECODE_PVRTC2_ROTATE_BLOCK_PAL),
	PYNOECONSTN(PVRTC_DECODE_PVRTC2_NO_OR_WITH_0_ALPHA),

	PYNOECONSTN(TEXRGBAFLOAT_FLAG_NOHDR),
	PYNOECONSTN(TEXRGBAFLOAT_FLAG_SCALEANDBIAS),
	PYNOECONSTN(TEXRGBAFLOAT_FLAG_RGB),
	PYNOECONSTN(TEXRGBAFLOAT_FLAG_TOLINEAR),
	PYNOECONSTN(TEXRGBAFLOAT_FLAG_TOGAMMA),
	PYNOECONSTN(TEXRGBAFLOAT_FLAG_NORMALIZE),

	PYNOECONSTN(kNHDRTF_RGB_F96),
	PYNOECONSTN(kNHDRTF_RGBA_F128),
	PYNOECONSTN(kNHDRTF_Lum_F32),
	PYNOECONSTN(kNHDRTF_RGBA_F64),

	PYNOECONSTN(NOE_ENCODEDXT_BC1),
	PYNOECONSTN(NOE_ENCODEDXT_BC2),
	PYNOECONSTN(NOE_ENCODEDXT_BC3),
	PYNOECONSTN(NOE_ENCODEDXT_BC4),
	PYNOECONSTN(NOE_ENCODEDXT_BC5),
	PYNOECONSTN(NOE_ENCODEDXT_BC6H),
	PYNOECONSTN(NOE_ENCODEDXT_BC6S),
	PYNOECONSTN(NOE_ENCODEDXT_BC7),

	PYNOECONSTN(TILE_CHOP_FLAG_MIRROR_X),
	PYNOECONSTN(TILE_CHOP_FLAG_MIRROR_Y),

The "rapi" module exposes the following methods:

	//core functionality
	//--
	{"getOutputName", Noesis_GetOutputName, METH_NOARGS, "returns destination filename."}, //args=none
	{"getInputName", Noesis_GetInputName, METH_NOARGS, "returns source filename."}, //args=none
	{"getLastCheckedName", Noesis_GetLastCheckedName, METH_NOARGS, "returns last checked/parsed filename."}, //args=none
	{"checkFileExt", Noesis_CheckFileExt, METH_VARARGS, "non-0 if filename contains extension. (uu)"}, //args=filename, extension
	{"getLocalFileName", Noesis_GetLocalFileName, METH_VARARGS, "returns local filename string. (u)"}, //args=full file path
	{"getExtensionlessName", Noesis_GetExtensionlessName, METH_VARARGS, "returns extensionless filename string. (u)"}, //args=filename
	{"getDirForFilePath", Noesis_GetDirForFilePath, METH_VARARGS, "returns directory string for filename. (u)"}, //args=filename
	{"lastCheckedPartialChecksum", Noesis_LastCheckedPartialChecksum, METH_VARARGS, "returns crc32 for a region of the last checked file, caching the result. returns None if operation fails. (ii)"}, //args=offset, size
	{"checkFileExists", Noesis_CheckFileExists, METH_VARARGS, "returns non-0 if file exists. (u)"}, //args=filename
	{"noesisIsExporting", Noesis_IsExporting, METH_NOARGS, "returns non-0 if the handler is invoked for an export target instead of a preview or instanced module data load."}, //args=none
	{"loadIntoByteArray", Noesis_LoadIntoByteArray, METH_VARARGS, "returns PyByteArray with file. (u)"}, //args=filename
	{"loadPairedFile", Noesis_LoadPairedFile, METH_VARARGS, "returns PyByteArray with file. (ss)"}, //args=file description, file extension
	{"loadPairedFileOptional", Noesis_LoadPairedFileOptional, METH_VARARGS, "same as loadPairedFile, but returns None on cancel/fail instead of raising an exception. (ss)"}, //args=file description, file extension
	{"loadPairedFileGetPath", Noesis_LoadPairedFileGetPath, METH_VARARGS, "same as loadPairedFile, but returns None on cancel/fail instead of raising an exception, and returns a tuple of (data, loadPath). (ss)"}, //args=file description, file extension
	{"loadFileOnTexturePaths", Noesis_LoadFileOnTexturePaths, METH_VARARGS, "checks all texture paths for files, and returns None or bytearray of loaded data. (s)"}, //args=file name
	{"simulateDragAndDrop", Noesis_SimulateDragAndDrop, METH_VARARGS, "simulates drag and drop using specified file. (s)"}, //args=file name
	{"processCommands", Noesis_ParseCommands, METH_VARARGS, "processes given commands in the active rapi module. (s)"}, //args=commands
	{"deferToOtherHandler", Noesis_DeferToOtherHandler, METH_VARARGS, "see comments around Noesis_DeferToOtherHandler in pluginshare.h. (sO)"}, //args=other format's description string, data

	{"exportArchiveFile", Noesis_ExportArchiveFile, METH_VARARGS, "exports an archive file. (sO)"}, //args=filename, data (PyBytes or PyByteArray)
	{"exportArchiveFileCheck", Noesis_ExportArchiveFileCheck, METH_VARARGS, "returns non-0 if calling exportArchiveFile on this path would overwrite. (s)"}, //args=filename
	{"exportArchiveFileGetName", Noesis_ExportArchiveFileGetName, METH_VARARGS, "returns absolute path for archive export file, creating directories as needed. (s)"}, //args=filename

	//image/array utility
	//--
	//swapEndianArray can be useful for things like 360 dxt data (swap count of 2)
	{"swapEndianArray", Noesis_SwapEndianArray, METH_VARARGS, "returns the entire array endian-swapped at x bytes. (Oi|ii)"}, //args=source array, swap count, (optional) offset (in bytes, into array), stride
	{"scaleAndBiasPackedFloats", Noesis_ScaleAndBiasPackedFloats, METH_VARARGS, "returns s&b on bytearray of packed floats, with optional clamping. (Off|ff)"}, //args=array, scale, bias, (optional) min value, max value
	{"imageResample", Noesis_ImageResample, METH_VARARGS, "returns a resampled (user-specified filtering, default bilinear) rgba/32bpp image in a bytearray. (Oiiii)"}, //args=source image array (must be rgba32), source width, source height, dest width, dest height
	{"imageResampleBox", Noesis_ImageResampleBox, METH_VARARGS, "returns a resampled rgba/32bpp image in a bytearray. (Oiiii)"}, //args=source image array (must be rgba32), source width, source height, dest width, dest height
	{"imageResampleNearest", Noesis_ImageResampleNearest, METH_VARARGS, "returns a resampled rgba/32bpp image in a bytearray. (Oiiii|i)"}, //args=source image array (must be rgba32), source width, source height, dest width, dest height, flags
	{"imageResampleBicubic", Noesis_ImageResampleBicubic, METH_VARARGS, "returns a resampled rgba/32bpp image in a bytearray. (Oiiii|f)"}, //args=source image array (must be rgba32), source width, source height, dest width, dest height, sharpness control 0..1 (functions as continuity on a Kochanek-Bartels curve)
	//imageMedianCut - pixel stride is expected to be 3 for rgb888 or 4 for rgba8888 data. desiredColors can be any number. if useAlpha is true (and pixStride is 4), the alpha channel will be considered in the process.
	//returned bytearray is in rgba32 form.
	{"imageMedianCut", Noesis_ImageMedianCut, METH_VARARGS, "returns a median-cut rgba/32bpp image in a bytearray. (Oiiiii)"}, //args=source image array (must be rgba32), pixel stride, width, height, dest width, dest height, desiredColors, alpha flag
	//imageGetPalette - source image must be rgba32. if clear flag is non-0, the first entry of the palette will be made black/clear. if alpha flag is 0, alpha will be ignored.
	{"imageGetPalette", Noesis_ImageGetPalette, METH_VARARGS, "returns a rgba/32bpp X-entry palette in a bytearray. (Oiiiii)"}, //args=source image array (must be rgba32), width, height, number of colors, clear flag, alpha flag
	//imageApplyPalette source image must be rgba32, as must palette.
	{"imageApplyPalette", Noesis_ImageApplyPalette, METH_VARARGS, "returns an indexed/8bpp image in a bytearray. (OiiOi)"}, //args=source image array (must be rgba32), width, height, rgba32 palette, number of palette entries
	//example python code to generate a 8bpp image with 256-color palette and convert it back to rgba32:
	//(the 256 in each call could also be replaced with 16 to generate 4bpp data)
	/*
	imgPal = rapi.imageGetPalette(imgPix, imgWidth, imgHeight, 256, 0, 1)
	idxPix = rapi.imageApplyPalette(imgPix, imgWidth, imgHeight, imgPal, 256)
	#the following takes the provided palette and 8bpp pixel array, and combines it back into a rgba32 pixel array
	for i in range(0, imgWidth*imgHeight):
		imgPix[i*4 + 0] = imgPal[idxPix[i]*4 + 0]
		imgPix[i*4 + 1] = imgPal[idxPix[i]*4 + 1]
		imgPix[i*4 + 2] = imgPal[idxPix[i]*4 + 2]
		imgPix[i*4 + 3] = imgPal[idxPix[i]*4 + 3]
	*/
	//imageEncodeRaw/imageDecodeRaw - format string is in the format of "rx gx bx ax", where x is the number of bits taken by that component. does not automatically pad to byte boundaries between pixels. (use p if padding is desired)
	//omitting a component from the format string will mean the component is 0 (or in the case of alpha, 255) in the destination buffer.
	//component ordering also dictates the source order, so a1r5b5g5 would be formatted as "a1 r5 g5 b5" (spaces optional)
	//you may also use p to denote padding. p may be used numerous times in the format string, so if you wanted only 7 bits of each component on a rgba32 image, you'd use: "p1r7p1g7p1b7p1a7"
	{"imageEncodeRaw", Noesis_ImageEncodeRaw, METH_VARARGS, "returns encoded image from rgba32. (Oiis)"}, //args=source image array, width, height, format string
	{"imageDecodeRaw", Noesis_ImageDecodeRaw, METH_VARARGS, "returns rgba32 image from decoded raw pixels. (Oiis|i)"}, //args=source image array, width, height, format string, optional flags
	{"imageDecodeRawPal", Noesis_ImageDecodeRawPal, METH_VARARGS, "returns rgba32 image from decoded raw pixels+palette. (OOiiis|i)"}, //args=source image array, source palette, width, height, bits per pixel, format string (for palette colors), optional flags (noesis.DECODEFLAG_* flags)
	{"imageToLinear", Noesis_ImageToLinear, METH_VARARGS, "returns rgba32 converted from gamma to linear space. (Oii)"}, //args=source image array, image width, image height
	{"imageToGamma", Noesis_ImageToGamma, METH_VARARGS, "returns rgba32 converted from linear to gamma space. (Oii)"}, //args=source image array, image width, image height
	{"imageScaleRGBA32", Noesis_ImageScaleRGBA32, METH_VARARGS, "returns scaled rgba32 data. (OOii|i)"}, //args=source image array, list/tuple/vec4 for rgba scale, image width, image height, optype (0=normal, 1=renormalize rgba instead of clipping each component, 2=pow instead of scale)
	{"imageFlipRGBA32", Noesis_ImageFlipRGBA32, METH_VARARGS, "returns flipped rgba32 data. (Oiiii)"}, //args=source image array, width, height, horizontal flip flag, vertical flip flag
	{"imageGaussianBlur", Noesis_ImageGaussianBlur, METH_VARARGS, "returns gaussian-blurred rgba32 data from rgba32 source. (Oiif)"}, //args=source image array, width, height, sigma
	{"imageNormalMapFromHeightMap", Noesis_ImageNormalMapFromHeightMap, METH_VARARGS, "returns normal map rgba32 data from rgba32 source. (Oiiffi)"}, //args=image array, width, height, height scale, texel scale, (optional) flags
	{"imagePrefilterRoughness", Noesis_ImagePrefilterRoughness, METH_VARARGS, "returns filtered roughness image, same size/channels as source. (OiiifOiiii)"}, //args=image array, width, height, roughness channel, roughness scale, normals, normals width, normals height, type, flags
	{"imageInterpolatedSample", Noesis_ImageInterpolatedSample, METH_VARARGS, "returns a rgba tuple (in 0.0-1.0 range) of the interpolated sample from a rgba32 image (Oiiff)"}, //args=image array, width, height, x fraction, y fraction
	{"imageCopyChannelRGBA32", Noesis_ImageCopyChannelRGBA32, METH_VARARGS, "returns rgba32 image with channel copied. (Oii)"}, //args=image array, source channel index, dest channel index
	{"imageSwapChannelRGBA32", Noesis_ImageSwapChannelRGBA32, METH_VARARGS, "returns rgba32 image with channels swapped. (Oii)"}, //args=image array, channel index a, channel index b
	{"imageShiftUpTo8", Noesis_ImageShiftUpTo8, METH_VARARGS, "returns image with each channel shifted up to 8 bits. (Oiiii)"}, //args=image array, width, height, channel count, shift amount
	{"imageOpaqueAlphaRGBA32", Noesis_ImageOpaqueAlphaRGBA32, METH_VARARGS, "returns true if alpha is opaque. (O)"}, //args=rgba32 data
	//example python code convert to r5g5b5a1 from rgba32, then go back to rgba32 from r5g5b5a1
	//imgPix = rapi.imageEncodeRaw(imgPix, imgWidth, imgHeight, "r5g5b5a1")
	//imgPix = rapi.imageDecodeRaw(imgPix, imgWidth, imgHeight, "r5g5b5a1")
	{"imageDecodeDXT", Noesis_ImageDecodeDXT, METH_VARARGS, "returns rgba32 image from decoded dxt. (Oiii)"}, //args=source image array, width, height, dxt format (may be one of the noesis.NOESISTEX_DXT* constants or a FOURCC code)
	{"imageEncodeDXT", Noesis_ImageEncodeDXT, METH_VARARGS, "returns encoded dxt from rgba image. (Oiiii)"}, //args=source image array, source pixel stride in bytes, width, height, dxt format (may be one of the noesis.NOE_ENCODEDXT_* constants)
	{"imageDecodePVRTC", Noesis_ImageDecodePVRTC, METH_VARARGS, "returns rgba32 image from decoded pvrtc. (Oiii)"}, //args=source image array, width, height, bits per pixel
	{"imageDecodeASTC", Noesis_ImageDecodeASTC, METH_VARARGS, "returns rgba32 image from decoded astc. (Oiiiiii)"}, //args=source image array, block width, block height, block depth, width, height, depth
	{"imageEncodeASTC", Noesis_ImageEncodeASTC, METH_VARARGS, "returns encoded astc from rgba image. (Oiiiiiii)"}, //args=source image array, block width, block height, block depth, width, height, depth, quality
	{"imageDecodeETC", Noesis_ImageDecodeETC, METH_VARARGS, "returns rgba32 image from decoded etc. (Oiis)"}, //args=source image array, width, height, format string (e.g. "R", "RG", "Rs", "RGs", "RGB", "RGB1", "sRGB", "RGBA", "sRGBA", "RGBA1", "sRGBA1")
	{"imageEncodeETC", Noesis_ImageEncodeETC, METH_VARARGS, "returns encoded etc from rgba image. (Oiiii|i)"}, //args=source image array, width, height, format (0..11), quality, (optional) flags
	{"imageDecodePICA200ETC1", Noesis_ImageDecodePICA200ETC1, METH_VARARGS, "returns rgba decoded from specialized PICA200 ETC1, may be in ETC1-A4 form. (Oiii|i)"}, //args=source image data, width, height, alpha flag (1 if alpha, 0 if none), (optional) flags - see notes in pluginshare.h for more details
	{"imageUntile360Raw", Noesis_ImageUntile360Raw, METH_VARARGS, "returns untiled raw pixel data. (Oiii)"}, //args=source image array, width, height, bytes per pixel
	{"imageUntile360DXT", Noesis_ImageUntile360DXT, METH_VARARGS, "returns untiled dxt pixel data. (Oiii)"}, //args=source image array, width, height, block size (e.g. 8 for dxt1, 16 for dxt5)
	{"imageUntile1dThin", Noesis_ImageUntile1dThin, METH_VARARGS, "returns untiled data. (Oiiii)"}, //args=source image data, width, height, bits per texel, block compressed flag
	{"imageTile1dThin", Noesis_ImageTile1dThin, METH_VARARGS, "returns untiled data. (Oiiii)"}, //args=source image data, width, height, bits per texel, block compressed flag
	{"imageUntileBlockLinearGOB", Noesis_UntileBlockLinearGOB, METH_VARARGS, "returns untiled data. (Oiii|i)"}, //args=source image data, width, height, bytes per element, (optional) block height
	{"imageTileBlockLinearGOB", Noesis_TileBlockLinearGOB, METH_VARARGS, "returns untiled data. (Oiii|i)"}, //args=source image data, width, height, bytes per element, (optional) block height
	{"imageBlockLinearGOBBlockHeight", Noesis_BlockLinearGOBBlockHeight, METH_VARARGS, "returns block height given image height and log2 of max block height. (ii)"}, //args=height, log2 of max block height
	{"imageBlockLinearGOBMaxBlockHeight", Noesis_BlockLinearGOBMaxBlockHeight, METH_VARARGS, "returns log2 of mip0's max block height for default layout under Some Drivers. (i|i)"}, //args=height, (optional) log2 of min block height, default 0
	{"imageUntwiddlePSP", Noesis_ImageUntwiddlePSP, METH_VARARGS, "returns untwiddled (psp hardware) texture data. (Oiii)"}, //args=source image array, width, height, bits (not bytes) per pixel
	{"imageUntwiddlePS2", Noesis_ImageUntwiddlePS2, METH_VARARGS, "returns untwiddled (ps2 hardware) texture data. (Oiii)"}, //args=source image array, width, height, bits (not bytes) per pixel. bpp must be 4/8/16/32.
	{"imageTwiddlePS2", Noesis_ImageTwiddlePS2, METH_VARARGS, "returns twiddled (ps2 hardware) texture data. (Oiii)"}, //args=source image array, width, height, bits (not bytes) per pixel. bpp must be 4 or 8.
	{"imagePS2WriteAndReadback32", Noesis_ImagePS2WriteAndReadback32, METH_VARARGS, "returns untwiddled (ps2 hardware) texture data. (Oiiiii)"}, //args=source image array, write width, write height, width, height, bits (not bytes) per pixel.
	{"imageFromMortonOrder", Noesis_ImageToMortonOrder, METH_VARARGS, "returns linear image data. (Oii|ii)"}, //args=source image array, width, height, (optional) bytes per pixel, inferred from array size if not specified, (optional) additional flags
	{"imageToMortonOrder", Noesis_ImageFromMortonOrder, METH_VARARGS, "returns morton ordered image data. (Oii|ii)"}, //args=source image array, width, height, (optional) bytes per pixel, inferred from array size if not specified, (optional) additional flags
	{"imageUntilePICA200Raw", Noesis_ImageUntilePICA200Raw, METH_VARARGS, "returns untiled raw data. (Oiii|i)"}, //args=source image data, width, height, bytes per pixel, (optional) flags - see notes in pluginshare.h for more details
	{"imageTilePICA200Raw", Noesis_ImageTilePICA200Raw, METH_VARARGS, "returns tiled raw data. (Oiii|i)"}, //args=source image data, width, height, bytes per pixel, (optional) flags - see notes in pluginshare.h for more details
	{"imageUntilePICA200ETC", Noesis_ImageUntilePICA200ETC, METH_VARARGS, "returns untiled ETC data. (Oiii|i)"}, //args=source image data, width, height, bytes per pixel, (optional) flags - see notes in pluginshare.h for more details
	{"imageTilePICA200ETC", Noesis_ImageTilePICA200ETC, METH_VARARGS, "returns tiled ETC data. (Oiii|i)"}, //args=source image data, width, height, bytes per pixel, (optional) flags - see notes in pluginshare.h for more details
	{"imageUntileAMDR600", Noesis_ImageUntileAMDR600, METH_VARARGS, "returns tuple of untiled data, pitch, slice size. see pluginshare.h for more information. (Oiiiiiiii)"}, //args=source image data, width, height, depth, mip index, format, type, swizzle, tile mode
	{"imageTileAMDR600", Noesis_ImageTileAMDR600, METH_VARARGS, "returns tuple of tiled data, pitch, slice size. see pluginshare.h for more information. (Oiiiiiiii)"}, //args=source image data, width, height, depth, mip index, format, type, swizzle, tile mode
	{"imageUntileAMDRDNA", Noesis_ImageUntileAMDRDNA, METH_VARARGS, "returns untiled data. see pluginshare.h for more information. (Oiiiiii)"}, //args=source image data, width, height, block width, block height, tile mode, bytes per element
	{"imageTileAMDRDNA", Noesis_ImageTileAMDRDNA, METH_VARARGS, "returns tiled data. see pluginshare.h for more information. (Oiiiiii)"}, //args=source image data, width, height, block width, block height, tile mode, bytes per element
	{"imageCalculateAMDRDNAMipInfo", Noesis_CalculateAMDRDNAMipInfo, METH_VARARGS, "returns tuple of (mip offset, width in elements, height in elements, block width, block height, bytes per element). (iiiiii)"}, //args=tile mode, data format, width, height, mip index, mip count
	{"imageNormalSwizzle", Noesis_ImageNormalSwizzle, METH_VARARGS, "returns rgba32 image with various pixel processing. also auto-normalizes pixels. (Oiiiii)"}, //args=source image array (must be rgba32), width, height, swap alpha-red flag (0 or 1), derive b/z flag (0 or 1), signed flag (0 or 1)
	{"imageExpandU8Normals", Noesis_ImageExpandU8Normals, METH_VARARGS, "returns expanded, normalized vectors as f32 packed in bytearray. (Oiii)"}, //args=source image array, width, height, elements per normal (min 3)
	{"imagePackU8Normals", Noesis_ImagePackU8Normals, METH_VARARGS, "returns bytearray of packed normal vectors. (Oiii)"}, //args=source normals (bytearray of packed f32 xyz), width, height, elements per normal (min 3, max 4)
	{"imageTransformTangentSpaceNormals", Noesis_ImageTransformTangentSpaceNormals, METH_VARARGS, "returns model space vectors as f32 packed in bytearray. (OiiO)"}, //args=f32 normals packed in bytearray, width, height, packed uv-tangent vertices in triangle list order
	{"imageGetDDSFromDXT", Noesis_ImageGetDDSFromDXT, METH_VARARGS, "returns a dds file in a bytearray, from dxt data and supplied parameters. (Oiiii)"}, //args=source image array, width, height, number of mipmaps, dxt format (may be one of the noesis.NOESISTEX_DXT* constants or a FOURCC code)
	{"imageGetTGAFromRGBA32", Noesis_ImageGetTGAFromRGBA32, METH_VARARGS, "returns a tga file in a bytearray, from rgba32 data and supplied parameters. (Oii)"}, //args=source image array, width, height
	{"imageGetTexRGBA", Noesis_ImageGetTexRGBA, METH_VARARGS, "gets rgba32 pixel data for a texture object. (O)"}, //args=NoeTexture
	{"imageGetTexRGBAFloat", Noesis_ImageGetTexRGBAFloat, METH_VARARGS, "gets rgba32 float data (normally 0..1, but may be signed or exceed this range for hdr data) for a texture object. (O|ii)"}, //args=NoeTexture, (optional) flags, offset
	{"imageBlit32", Noesis_ImageBlit32, METH_VARARGS, "image blit between 2 32-bit images. (OiiiiOiiii|ii)"}, //args=destination image, destination width, destination height, destination x offset, destination y offset, source image, source width, source height, source x offset, source y offset, (optional) dest stride, source stride (if not provided, assumed to be width*4)
	{"imageTileInto32", Noesis_ImageTileInto32, METH_VARARGS, "tiles image into another. (OiiOiiii)"}, //args=destination image, destination width, destination height, source image, source width, source height, horizontal wrap/mirror flags, vertical wrap/mirror flags
	{"imageKernelProcess", Noesis_ImageKernelProcess, METH_VARARGS, "returns a processed image, processed by invoking a provided kernel method which operates on a bytearray containing data for the active pixel. (OiiiO|O)"}, //args=destination image, width, height, bytes per pixel, kernel method (should be implemented as def kernelMethod(imageData (original image), offset (current processing offset into image), kernelData (bytes of data to operate on), userData), (optional) user data
	{"imageDrawText8x8", Noesis_ImageDrawText8x8, METH_VARARGS, "draws text into rgba32 with 8x8 font. (OiiiiiOs)"}, //args=rgba32 dest, width, height, x, y, flags, rgb list (list/tuple of 3 0..255 values), text
	{"imageChopTiles8x8", Noesis_ImageChopTiles8x8, METH_VARARGS, "returns tuple of bytes, (int32 tile references, unique 8x8 tiles). (Oiii)"}, //args=8-bit image, width, height, flags (1=no mirroring)
	{"imageArrangeTiles", Noesis_ImageArrangeTiles, METH_VARARGS, "returns image with tiles arranged using the provided LUT. (OiiiiO)"}, //args=image data, bytes per pixel, tile width, tile height, page width, LUT (list/tuple)
	{"imageDXTRemoveFlatFractionBlocks", Noesis_ImageRemoveFlatFractionBlocks, METH_VARARGS, "performs processing to turn dxt fraction-only blocks into direct color reference blocks for shitty hardware. (Oi)"}, //args=dxt data, texture format (must be one of the noesis.NOESISTEX_DXT* constants)
	{"imageN64ReadTMEM", Noesis_ImageN64ReadTMEM, METH_VARARGS, "simulate read from tmem. (Oiii)"}, //args=bytes, width, height, bpp
	{"imageN64WriteTMEM", Noesis_ImageN64WriteTMEM, METH_VARARGS, "simulate write to tmem. (Oiii)"}, //args=bytes, width, height, bpp
	{"imageN64DecodeRGBA32", Noesis_ImageN64DecodeRGBA32, METH_VARARGS, "returns decoded rgba32 image. (OOiiiii)"}, //args=tex data, pal data, width, height, color format, bpp (0-3), flags
	{"imageGenVDPDrawTile", Noesis_ImageGenVDPDrawTile, METH_VARARGS, "draws tile to rgba32 canvas. (OiiiiHOOi|ii)"}, //args=rgba32 dest, width, height, x, y, tile data, char buffer, pal buffer, flags, (optional) width in tiles, height in tiles
	{"imageGenVDPDecodeChar", Noesis_ImageGenVDPDecodeChar, METH_VARARGS, "returns bytearray of decoded linear 8bpp image(s). (O)"}, //args=8x8 4-bit source image(s)
	{"imageGenVDPEncodeChar", Noesis_ImageGenVDPEncodeChar, METH_VARARGS, "returns bytearray of encoded 4bpp image(s). (O)"}, //args=8x8 8-bit linear source image(s)
	{"imageGenVDPExpandPalette", Noesis_ImageGenVDPExpandPalette, METH_VARARGS, "returns colors expanded to rgba32. (Oi)"}, //args=palette, color ramp index
	{"imageGameBoyDrawTile", Noesis_ImageGameBoyDrawTile, METH_VARARGS, "draws tile to rgba32 canvas. (OiiiiiiOOi)"}, //args=rgba32 dest, width, height, x, y, char index, tile data, char buffer, pal buffer, flags
	{"imageNESDrawTile", Noesis_ImageNESDrawTile, METH_VARARGS, "draws tile to rgba32 canvas. (OiiiiiOOi)"}, //args=rgba32 dest, width, height, x, y, char index, char buffer, pal buffer, flags
	{"imageNESEncodeChar32", Noesis_ImageNESEncodeChar32, METH_VARARGS, "encodes NES char from rgba32. (OOi)"}, //args=rgba32 image, rgb24 pallete (used to match color to index), flags
	{"imageSNESMode1B0DrawTile", Noesis_ImageSNESMode1B0DrawTile, METH_VARARGS, "draws tile to rgba32 canvas. (OiiiiHOOi)"}, //args=rgba32 dest, width, height, x, y, tile data, char buffer, pal buffer, flags
	{"imageSNESMode4B0DrawTile", Noesis_ImageSNESMode4B0DrawTile, METH_VARARGS, "draws tile to rgba32 canvas. (OiiiiHOOi)"}, //args=rgba32 dest, width, height, x, y, tile data, char buffer, pal buffer, flags
	{"imageSNESExpandPalette", Noesis_ImageSNESExpandPalette, METH_VARARGS, "returns colors expanded to rgba32. (Oi)"}, //args=palette, color ramp index
	{"imageSNESDecodeCharMode1B0", Noesis_ImageSNESDecodeCharMode1B0, METH_VARARGS, "returns bytearray of decoded linear 8bpp image(s). (O)"}, //args=8x8 4-bit source image(s)
	{"imageSNESEncodeCharMode1B0", Noesis_ImageSNESEncodeCharMode1B0, METH_VARARGS, "returns bytearray of encoded 4bpp image(s). (O)"}, //args=8x8 8-bit linear source image(s)
	{"imageSNESDecodeCharMode4B0", Noesis_ImageSNESDecodeCharMode4B0, METH_VARARGS, "returns bytearray of decoded linear 8bpp image(s). (O)"}, //args=8x8 8-bit source image(s)
	{"imageSNESEncodeCharMode4B0", Noesis_ImageSNESEncodeCharMode4B0, METH_VARARGS, "returns bytearray of encoded 8bpp image(s). (O)"}, //args=8x8 8-bit linear source image(s)
	{"imageJaguarCRYToRGBA", Noesis_ImageJaguarCRYToRGBA, METH_VARARGS, "returns bytearray of rgba32 data. (Oi)"}, //args=bytearray of CRY data, flags
	{"imageJaguarRGBAToCRY", Noesis_ImageJaguarRGBAToCRY, METH_VARARGS, "returns bytearray of cry data. (Oi)"}, //args=bytearray of RGB data, flags
	{"imageJaguarDecodeWidth", Noesis_ImageJaguarDecodeWidth, METH_VARARGS, "returns decoded 6-bit width. (i)"}, //args=encoded width
	{"imageJaguarClosestWidth", Noesis_ImageJaguarClosestWidth, METH_VARARGS, "returns closest addressable width to the provided width, encoded. (i)"}, //args=width
	{"imageK052109DrawTile", Noesis_ImageK052109DrawTile, METH_VARARGS, "draws tile to rgba32 canvas. (OiiiiHOOiii)"}, //args=rgba32 dest, width, height, x, y, tile data, char buffer, pal buffer, $x6B00 (tmnt, may be mapped elsewhere for other machines) value, $x6E00 value, flags

	{"imageWritePNGBuffer", Noesis_ImageWritePNGBuffer, METH_VARARGS, "returns png in memory buffer. (Oii)"}, //args=source rgba, width, height

	{"imagePSXDecodeVideoFrame", Noesis_ImagePSXDecodeVideoFrame, METH_VARARGS, "returns MDEC data for every macroblock in the frame. (Oiiii)"}, //args=frame data, frame version, frame width, frame height, quantization scale
	{"imagePSXMDEC", Noesis_ImagePSXMDEC, METH_VARARGS, "processes MDEC blocks and returns rgba32 canvas. (OOOOii)"}, //args=mdec block data, inverse dct matrix as bytearray of 8x8 int16s (may be None), bytearray of chroma quantization scales, bytearray of luma quantization scales, width, height

	//data compression/decompression
	//--
	{"decompInflate", Noesis_DecompInflate, METH_VARARGS, "returns decompressed bytearray. (Oi|i)"}, //args=source bytes, destination size, (optional) window size
	{"decompPuff", Noesis_DecompPuff, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size
	{"decompBlast", Noesis_DecompBlast, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size
	{"decompLZS01", Noesis_DecompLZS01, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size
	{"decompFPK", Noesis_DecompFPK, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size
	{"decompLZO", Noesis_DecompLZO, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size
	{"decompLZO2", Noesis_DecompLZO2, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size
	{"decompLZHMelt", Noesis_DecompLZHMelt, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size
	{"decompXMemLZX", Noesis_DecompXMemLZX, METH_VARARGS, "returns decompressed bytearray. (Oi|iii)"}, //args=source bytes, destination size. optional: window bits (default 17), reset interval (default -1), frame size (default -1)
	{"decompPRS", Noesis_DecompPRS, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size.
	{"decompLZ4", Noesis_DecompLZ4, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size.
	{"decompLZMA", Noesis_DecompLZMA, METH_VARARGS, "returns decompressed bytearray. (OiO)"}, //args=source bytes, destination size, props bytes.
	{"decompLZNT1", Noesis_DecompLZNT1, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size.
	{"decompLZJag", Noesis_DecompLZJAG, METH_VARARGS, "returns decompressed bytearray. (Oi|iii)"}, //args=source bytes, destination size, (optional) index bits, length bits, breakeven
	{"getInflatedSize", Noesis_GetInflatedSize, METH_VARARGS, "walks through deflate stream to return final decompressed size. (O|i)"}, //args=source bytes, (optional) window bits
	{"getLZHMeltSize", Noesis_GetLZHMeltSize, METH_VARARGS, "walks through lzh stream to return final decompressed size. (O)"}, //args=source bytes
	{"getLZNT1Size", Noesis_GetLZNT1Size, METH_VARARGS, "walks through lzh stream to return final decompressed size. (O)"}, //args=source bytes
	{"getPRSSize", Noesis_GetPRSSize, METH_VARARGS, "walks through prs stream to return final decompressed size. (O)"}, //args=source bytes
	{"getLZJagSize", Noesis_GetLZJagSize, METH_VARARGS, "walks through lzjag stream to return final decompressed size. (O|iii)"}, //args=source bytes, (optional) index bits, length bits, breakeven
	{"decryptAES", Noesis_DecryptAES, METH_VARARGS, "returns decrypted bytearray. (OO|O)"}, //args=source bytes, key, IV (may be None)
	{"encryptAES", Noesis_EncryptAES, METH_VARARGS, "returns encrypted bytearray. (OO|O)"}, //args=source bytes, key, IV (may be None)

	{"compressDeflate", Noesis_CompressDeflate, METH_VARARGS, "returns compressed bytearray. (O|i)"}, //args=source bytes, (optional) window size

	{"compressHuffmanCanonical", Noesis_CompressHuffmanCanonical, METH_VARARGS, "returns compressed bytearray. (O)"}, //args=source bytes
	{"decompHuffmanCanonical", Noesis_DecompHuffmanCanonical, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size
	{"decompRNC", Noesis_DecompRNC, METH_VARARGS, "returns decompressed bytearray. (Oi)"}, //args=source bytes, destination size

	{"mw_tw_dmagfxcopy", Noesis_MwTW_DmaGfxCopy, METH_VARARGS, "does t/w-unit copy into canvas. (OiiiiOOiiii)"}, //args=rgba32 dest, dest x, dest y, dest width, dest height, rgba32 palette, source data, dma control bits, source offset (in bits), source width, source height

	//geometry/misc utility
	//--
	//getFlatWeights - e.g. wbytes = getFlatWeights(vertWeights, 4)
	{"getFlatWeights", Noesis_GetFlatWeights, METH_VARARGS, "returns byte array of flattened weights. (in the form of int bone indices for each vert, float weights for each vert) (Oi)"}, //args=list of NoeVertWeight, max weights (0 to use the max from the list)
	{"multiplyBones", Noesis_MultiplyBones, METH_VARARGS, "returns a list of NoeBones multiplied according to hierarchy. (O)"}, //args=list of NoeBone objects
	{"createTriStrip", Noesis_CreateTriStrip, METH_VARARGS, "returns a list of triangle strip indices. (O|i)"}, //args=list of triangle list indices, optional WORD specifying a strip termination value (if provided, strips are terminated with this value instead of degenerate faces)
	{"createBoneMap", Noesis_CreateBoneMap, METH_VARARGS, "returns a list of mapped bone indices and remaps the provided weights. (O)"}, //args=list of NoeVertWeights
	{"dataToIntList", Noesis_DataToIntList, METH_VARARGS, "returns a list of ints interpreted from raw data. (Oiii)"}, //args=bytearray, number of elements, RPGEODATA_ type, NOE_LITTLEENDIAN or NOE_BIGENDIAN
	{"dataToFloatList", Noesis_DataToFloatList, METH_VARARGS, "returns a list of floats interpreted from raw data. (Oiii|i)"}, //args=bytearray, number of elements, RPGEODATA_ type, NOE_LITTLEENDIAN or NOE_BIGENDIAN, (optional) scale and bias unsigned values into -1 to 1 range if 1
	{"decodeNormals32", Noesis_DecodeNormals32, METH_VARARGS, "returns a bytearray of decoded floating point normals. (Oiiiii)"}, //args=original buffer of 32-bit normals, stride, x bits, y bits, z bits, source endianness. x/y/z bit values can be negative to indicate a signed component.
	{"decodeTangents32", Noesis_DecodeTangents32, METH_VARARGS, "returns a bytearray of decoded floating point tangents. (Oiiiii)"}, //args=original buffer of 32-bit normals, stride, x bits, y bits, z bits, w bits, source endianness. x/y/z/w bit values can be negative to indicate a signed component.
	{"decompressEdgeIndices", Noesis_DecompressEdgeIndices, METH_VARARGS, "returns a bytearray of decompressed little-endian short indices. (Oi|i)"}, //args=compressed data, number of indices to be decompressed, (optional) source endianness (NOE_LITTLEENDIAN or NOE_BIGENDIAN)
	{"tangentMatricesToTan4", Noesis_TangentMatricesToTan4, METH_VARARGS, "returns a bytearray of tan4 as float*4*vertcount. (iOiiOiiOii)"}, //args=vert count, normal buffer, normal RPGEODATA_ type, normal stride, tangent buffer, tangent RPGEODATA_ type, tangent stride, bitangent buffer, bitangent RPGEODATA_ type, bitangent stride
	{"blinnPhongToBeckmann", Noesis_BlinnPhongToBeckmann, METH_VARARGS, "returns beckmann roughness from blinn-phong specular exponent. (f)"}, //args=spec exponent
	{"beckmannToBlinnPhong", Noesis_BeckmannToBlinnPhong, METH_VARARGS, "returns blinn-phong specular exponent from beckmann roughness. (f)"}, //args=spec exponent
	{"isGeometryTarget", Noesis_IsGeometryTarget, METH_NOARGS, "returns 1 if the active format is a geometry target, otherwise 0."}, //args=none
	{"setDeferredAnims", Noesis_SetDeferredAnims, METH_VARARGS, "sets deferred anim data for a list of NoeAnim objects."}, //args=list of NoeAnim
	{"getDeferredAnims", Noesis_GetDeferredAnims, METH_NOARGS, "returns a list of NoeAnim objects. (or an empty list, if no deferred data is available)"}, //args=none
	{"loadExternalTex", Noesis_LoadExternalTex, METH_VARARGS, "returns a NoeTexture, or None if the texture could not be found. (s)"}, //args=name/path of texture, without extension
	{"loadTexByHandler", Noesis_LoadTexByHandler, METH_VARARGS, "returns a NoeTexture, or None if the texture could not be found. (Os|i)"}, //args=source bytes, desired extension, (optional) flags
	{"loadMdlTextures", Noesis_LoadMdlTextures, METH_VARARGS, "returns a tuple of NoeTextures, where all textures have already been converted to raw RGBA32. Sets the texRefIndex member of every NoeMesh in the model to the index of its texture in the returned tuple. (O)"}, //args=NoeModel, desired extension
	{"unpackPS2VIF", Noesis_UnpackPS2VIF, METH_VARARGS, "returns a tuple of NoePS2VIFUnpacks (O)"}, //args=vifcode data in byte form
	{"decodePSPVert", Noesis_DecodePSPVert, METH_VARARGS, "returns a NoePSPVertInfo (I)"}, //args=32-bit vertex tag
	{"splineToMeshBuffers", Noesis_SplineToMeshBuffers, METH_VARARGS, "returns a tuple of vertex and index data bytearrays. (OOiffi)"}, //args=spline, transform matrix, reverse triangle winding if 1, step size, size, subdivisions
	{"mergeKeyFramedFloats", Noesis_MergeKeyFramedFloats, METH_VARARGS, "returns a list of keyframes with n-element values given a list of keyframe floats, using linear interpolation to match keyframe times. (O)"}, //args=list of keyframed floats

	{"decodeADPCMBlock", Noesis_DecodeADPCMBlock, METH_VARARGS, "decodes an adpcm block. (OiiiiOOO|iid)"}, //args=data, bits per sample, num samples to decode, lshift, filter, filter table 0 (old sample) list, filter table 1 (older sample) list, list of 2 previous samples (will be modified), (optional) bit offset, bit stride, sample scale
	{"decodeXboxADPCMBlock", Noesis_DecodeXboxADPCMBlock, METH_VARARGS, "decodes an xbox adpcm block. (Oi)"}, //args=data, channel count
	{"writePCMWaveFile", Noesis_WritePCMWaveFile, METH_VARARGS, "writes pcm wave file with provided data. (uOiii)"}, //args=filename, data, bitrate, samplerate, channelcount
	{"createPCMWaveHeader", Noesis_CreatePCMWaveHeader, METH_VARARGS, "returns a bytearray of pcm wave header data. (iiii)"}, //args=data size, bitrate, samplerate, channelcount

	{"elfLoaderInit", Noesis_ElfLoaderInit, METH_VARARGS, "returns a handle to the elf loader. (KI)"}, //args=memory size, flags
	{"elfLoaderFree", Noesis_ElfLoaderFree, METH_VARARGS, "frees the elf loader and associated resources. (O)"}, //args=elf loader handle
	{"elfLoaderLoadPath", Noesis_ElfLoaderLoadPath, METH_VARARGS, "loads an ELF file on the provided path. (Ou|I)"}, //args=elf loader handle, path to elf file, (optional) flags
	{"elfLoaderLoadData", Noesis_ElfLoaderLoadData, METH_VARARGS, "loads an ELF file from the provided data. (OO|I)"}, //args=elf loader handle, bytes/bytearray object, (optional) flags
	{"elfLoaderSymbolCount", Noesis_ElfLoaderSymbolCount, METH_VARARGS, "returns the number of symbols loaded across ELF files. (O)"}, //args=elf loader handle
	{"elfLoaderSymbolInfo", Noesis_ElfLoaderSymbolInfo, METH_VARARGS, "returns a tuple of (name, address, size, packinfo). (OI)"}, //args=elf loader handle, symbol index
	{"elfLoaderSectionCount", Noesis_ElfLoaderSectionCount, METH_VARARGS, "returns the number of sections for the most recently loaded ELF. (O)"}, //args=elf loader handle
	{"elfLoaderSectionInfo", Noesis_ElfLoaderSectionInfo, METH_VARARGS, "returns a tuple of (name, virtual address, file offset, loaded address, size). (OI)"}, //args=elf loader handle, section index
	{"elfLoaderResetLoadedSectionSize", Noesis_ElfLoaderResetLoadedSectionSize, METH_VARARGS, "resets loader's loaded section size. (only affects loading when ignoring section load addresses) (O)"}, //args=elf loader handle
	{"elfLoaderReadMemory", Noesis_ElfLoaderReadMemory, METH_VARARGS, "returns data read from elf loader memory. (OKK)"}, //args=elf loader handle, read address, read size

	//setPreviewOption - allows the following options (list may or may not be outdated at any given time)
	//"drawAllModels"						"0"/"1" (toggles drawing all models at once in preview mode by default)
	//"noTextureLoad"						"0"/"1" (toggles auto-loading of textures for previewed model based on tex/mat names)
	//"setAnimPlay"							"0"/"1" (if 1, auto-starts animation in preview)
	//"setAnimSpeed"						"<val>" (set frames per second for preview animation playback to <val>)
	//"setAngOfs"							"x y z" (set default preview angle offset to x y z)
	{"setPreviewOption", Noesis_SetPreviewOption, METH_VARARGS, "sets various preview options. (ss)"}, //args=optName, optVal
	{"callExtensionMethod", Noesis_CallExtensionMethod, METH_VARARGS, "calls an extension method. (s|)"}, //args=optName, ... (other arguments depend on extension being called)
	{"createProceduralAnim", Noesis_CreateProceduralAnim, METH_VARARGS, "generates a procedural animation. (OOi)"}, //args=NoeBone list, NoeProceduralAnim list, numFrames
	{"forcePreviewAnimUI", Noesis_ForcePreviewAnimUI, METH_NOARGS, "forces the animation UI to appear in the active preview."}, //args=none

	{"toolLoadGData", Noesis_ToolLoadGData, METH_VARARGS, "sets the module into global data mode and loads a file. this should only be invoked by tools, do not invoke it in format handlers or you will probably crash noesis. returns True on success. (s)"}, //args=filename
	{"toolFreeGData", Noesis_ToolFreeGData, METH_NOARGS, "frees global data, must be used after toolLoadGData."}, //args=none
	{"toolSetGData", Noesis_ToolSetGData, METH_VARARGS, "same as toolLoadGData, but allows you to set the gdata from a model list. (O)"}, //args=list of NoeModel
	{"toolExportGData", Noesis_ToolExportGData, METH_VARARGS, "exports loaded gdata to given file. returns true on success. (ss)"}, //args=filename, options
	{"toolGetLoadedModelCount", Noesis_ToolGetLoadedModelCount, METH_NOARGS, "returns number of loaded models in gdata."}, //args=none
	{"toolGetLoadedModel", Noesis_ToolGetLoadedModel, METH_VARARGS, "returns NoeModel from gdata (i)."}, //args=model index
	{"toolSetSelectedModelIndex", Noesis_ToolSetSelectedModelIndex, METH_VARARGS, "sets selected model index in gdata (i)."}, //args=model index

	{"getInternalViewData", Noesis_GetInternalViewData, METH_NOARGS, "returns a buffer of internal view data, or None on failure. see pluginshare.h for more info."}, //args=none
	{"setInternalViewData", Noesis_SetInternalViewData, METH_VARARGS, "sets internal view data from a buffer, returns true if successful. see pluginshare.h for more info. (O)"}, //args=view data buffer

	{"parseInstanceOptions", Noesis_ParseInstanceOptions, METH_VARARGS, "parses option string in the active rapi instance. (s)"}, //args=options

	//rpg (Rich Procedural Geometry) interface
	//--
	//creates a rpg context. does not need to be explicitly freed in python, but make sure you don't grab any references to it and keep them outside of the method you created them in
	{"rpgCreateContext", RPGCreateContext, METH_NOARGS, "returns rpgeo context handle."}, //args=none
	//sets the active context
	{"rpgSetActiveContext", RPGSetActiveContext, METH_VARARGS, "sets the active context. (O)"}, //args=handle created by rpgCreateContext
	//All following rpg*/imm* functions operate on the active context and require no context handle to be passed in

	{"rpgReset", RPGReset, METH_NOARGS, "resets the active context."}, //args=none
	{"rpgSetMaterial", RPGSetMaterial, METH_VARARGS, "sets the material name. (s)"}, //args=string
	{"rpgSetLightmap", RPGSetLightmap, METH_VARARGS, "sets the lightmap/secondpass material name. (s)"}, //args=string
	{"rpgSetName", RPGSetName, METH_VARARGS, "sets the mesh name. (s)"}, //args=string
	{"rpgClearMaterials", RPGClearMaterials, METH_NOARGS, "clears all internal materials."}, //args=none
	{"rpgClearNames", RPGClearNames, METH_NOARGS, "clears all internal names."}, //args=none
	{"rpgClearMorphs", RPGClearMorphs, METH_NOARGS, "clears all internal morph buffers."}, //args=none
	{"rpgSetTransform", RPGSetTransform, METH_VARARGS, "sets geometry transform matrix. pass None to disable. (O)"}, //args=NoeMat43 or None
	{"rpgSetPosScaleBias", RPGSetPosScaleBias, METH_VARARGS, "sets geometry scale and bias - pass None, None to disable. (OO)"}, //args=NoeVec3 (scale), NoeVec3 (bias) - or None, None
	{"rpgSetUVScaleBias", RPGSetUVScaleBias, METH_VARARGS, "sets uv coordinate scale and bias - pass None, None to disable. (OO|i)"}, //args=NoeVec3 (scale), NoeVec3 (bias), optional uv index - or None, None
	{"rpgSetBoneMap", RPGSetBoneMap, METH_VARARGS, "provides an index map for vertex weight references to bone indices. (O)"}, //args=list of ints
	{"rpgSetOption", RPGSetOption, METH_VARARGS, "sets rpgeo option. (ii)"}, //args=option flag (one of the noesis.RPGOPT_ constants), option status (1=enabled, 0=disabled)
	{"rpgGetOption", RPGGetOption, METH_VARARGS, "returns 1 if option is enabled, otherwise 0. (i)"}, //args=option flag
	//rpgSetEndian/rpgSetTriWinding are now deprecated, use rpgSetOption instead
	{"rpgSetEndian", RPGSetEndian, METH_VARARGS, "sets endian mode for reading raw buffers. (i)"}, //args=0 - little endian or 1 - big endian
	{"rpgSetTriWinding", RPGSetTriWinding, METH_VARARGS, "sets triangle winding mode. (i)"}, //args=0 - normal or 1 - reverse winding
	{"rpgSetStripEnder", RPGSetStripEnder, METH_VARARGS, "sets the strip-reset value. (i)"}, //args=value
	{"rpgGetStripEnder", RPGGetStripEnder, METH_NOARGS, "returns the strip-reset value."}, //args=none

	//immediate-mode drawing in python works by feeding variable-sized component lists and/or tuples.
	//keep in mind that these values will not be normalized for you, even if they are provided as fixed-point.
	{"immBegin", IMMBegin, METH_VARARGS, "begin immediate-mode drawing. (i)"}, //args=primitive type
	{"immEnd", IMMEnd, METH_NOARGS, "end immediate-mode drawing."}, //args=none
	{"immVertex3", IMMVertex3, METH_VARARGS, "feeds a vertex position. (must be called last for each primitive) (O)"}, //args=3-component list
	{"immNormal3", IMMNormal3, METH_VARARGS, "feeds a vertex normal. (O)"}, //args=3-component list
	{"immTangent4", IMMTangent4, METH_VARARGS, "feeds a tangent vector. (O)"}, //args=4-component list, where 4th component is sign (-1 or 1) for bitangent
	{"immUV2", IMMUV2, METH_VARARGS, "feeds a vertex uv. (O)"}, //args=2-component list
	{"immLMUV2", IMMLMUV2, METH_VARARGS, "feeds a vertex lmuv. (O)"}, //args=2-component list
	{"immColor3", IMMColor3, METH_VARARGS, "feeds a vertex color. (O)"}, //args=3-component list
	{"immColor4", IMMColor4, METH_VARARGS, "feeds a vertex color. (O)"}, //args=4-component list
	{"immBoneIndex", IMMBoneIndex, METH_VARARGS, "feeds a vertex bone index. (O)"}, //args=x-component list
	{"immBoneWeight", IMMBoneWeight, METH_VARARGS, "feeds a vertex bone weight. (O)"}, //args=x-component list
	{"immVertMorphIndex", IMMVertMorphIndex, METH_VARARGS, "feeds a vertex morph index. (i)"}, //args=int
	//The following functions take raw bytes and decode them appropriately. Naming convention is #<type>, where # is number of elements and <type> is:
	//f - float
	//hf - half-float
	//b - byte
	//ub - unsigned byte
	//s - short
	//us - unsigned short
	//i - 32-bit int
	//ui - unsigned 32-bit int
	//X - arbitrary, you provide the RPGEODATA_ type and the number of elements.
	//All of these functions can also take an additional argument to specify an offset into the provided array of bytes.
	//For example, rapi.immVertex3f(positions[idx*12:idx*12+12]) could instead be rapi.immVertex3f(positions, idx*12), which is significantly less eye-raping and more efficient (as it requires no construction of a separate object for the slice)
	DEFINE_IMM_EX(immVertexX, IMMVertexX, METH_VARARGS, "feeds a vertex position. (must be called last for each primitive) (Oii)"), //args=bytes/bytearray of raw data, data type, number of elements
	DEFINE_IMM_EX(immVertex3f, IMMVertex3f, METH_VARARGS, "feeds a vertex position. (must be called last for each primitive) (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immVertex3us, IMMVertex3us, METH_VARARGS, "feeds a vertex position. (must be called last for each primitive) (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immVertex3s, IMMVertex3s, METH_VARARGS, "feeds a vertex position. (must be called last for each primitive) (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immVertex3hf, IMMVertex3hf, METH_VARARGS, "feeds a vertex position. (must be called last for each primitive) (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immNormalX, IMMNormalX, METH_VARARGS, "feeds a vertex normal. (Oii)"), //args=bytes/bytearray of raw data, data type, number of elements
	DEFINE_IMM_EX(immNormal3f, IMMNormal3f, METH_VARARGS, "feeds a vertex normal. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immNormal3us, IMMNormal3us, METH_VARARGS, "feeds a vertex normal. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immNormal3s, IMMNormal3s, METH_VARARGS, "feeds a vertex normal. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immNormal3hf, IMMNormal3hf, METH_VARARGS, "feeds a vertex normal. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immTangentX, IMMTangentX, METH_VARARGS, "feeds a tangent vector. (Oii)"), //args=bytes/bytearray of raw data, data type, number of elements
	DEFINE_IMM_EX(immTangent4f, IMMTangent4f, METH_VARARGS, "feeds a tangent vector. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immTangent4us, IMMTangent4us, METH_VARARGS, "feeds a tangent vector. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immTangent4s, IMMTangent4s, METH_VARARGS, "feeds a tangent vector. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immTangent4hf, IMMTangent4hf, METH_VARARGS, "feeds a tangent vector. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immUVX, IMMUVX, METH_VARARGS, "feeds a vertex uv. (Oii)"), //args=bytes/bytearray of raw data, data type, number of elements
	DEFINE_IMM_EX(immUV2f, IMMUV2f, METH_VARARGS, "feeds a vertex uv. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immUV2us, IMMUV2us, METH_VARARGS, "feeds a vertex uv. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immUV2s, IMMUV2s, METH_VARARGS, "feeds a vertex uv. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immUV2hf, IMMUV2hf, METH_VARARGS, "feeds a vertex uv. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immLMUVX, IMMLMUVX, METH_VARARGS, "feeds a vertex lmuv. (Oii)"), //args=bytes/bytearray of raw data, data type, number of elements
	DEFINE_IMM_EX(immLMUV2f, IMMLMUV2f, METH_VARARGS, "feeds a vertex lmuv. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immLMUV2us, IMMLMUV2us, METH_VARARGS, "feeds a vertex lmuv. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immLMUV2s, IMMLMUV2s, METH_VARARGS, "feeds a vertex lmuv. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immLMUV2hf, IMMLMUV2hf, METH_VARARGS, "feeds a vertex lmuv. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immColorX, IMMColorX, METH_VARARGS, "feeds a vertex color. (Oii)"), //args=bytes/bytearray of raw data, data type, number of elements
	DEFINE_IMM_EX(immColor3f, IMMColor3f, METH_VARARGS, "feeds a vertex color. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immColor3us, IMMColor3us, METH_VARARGS, "feeds a vertex color. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immColor3s, IMMColor3s, METH_VARARGS, "feeds a vertex color. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immColor3hf, IMMColor3hf, METH_VARARGS, "feeds a vertex color. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immColor4f, IMMColor4f, METH_VARARGS, "feeds a vertex color. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immColor4us, IMMColor4us, METH_VARARGS, "feeds a vertex color. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immColor4s, IMMColor4s, METH_VARARGS, "feeds a vertex color. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immColor4hf, IMMColor4hf, METH_VARARGS, "feeds a vertex color. (O)"), //args=bytes/bytearray of raw data
	DEFINE_IMM_EX(immBoneIndexX, IMMBoneIndexX, METH_VARARGS, "feeds a vertex bone index. (Oii)"), //args=bytes/bytearray of raw data, data type, number of elements
	DEFINE_IMM_EX(immBoneIndexub, IMMBoneIndexub, METH_VARARGS, "feeds a vertex bone index. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneIndexb, IMMBoneIndexb, METH_VARARGS, "feeds a vertex bone index. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneIndexus, IMMBoneIndexus, METH_VARARGS, "feeds a vertex bone index. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneIndexs, IMMBoneIndexs, METH_VARARGS, "feeds a vertex bone index. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneIndexui, IMMBoneIndexui, METH_VARARGS, "feeds a vertex bone index. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneIndexi, IMMBoneIndexi, METH_VARARGS, "feeds a vertex bone index. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneWeightX, IMMBoneWeightX, METH_VARARGS, "feeds a vertex bone weight. (Oii)"), //args=bytes/bytearray of raw data, data type, number of elements
	DEFINE_IMM_EX(immBoneWeightf, IMMBoneWeightf, METH_VARARGS, "feeds a vertex bone weight. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneWeightus, IMMBoneWeightus, METH_VARARGS, "feeds a vertex bone weight. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneWeightub, IMMBoneWeightub, METH_VARARGS, "feeds a vertex bone weight. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	DEFINE_IMM_EX(immBoneWeighthf, IMMBoneWeighthf, METH_VARARGS, "feeds a vertex bone weight. (Oi)"), //args=bytes/bytearray of raw data, number of elements
	{"immUserData", IMMUserData, METH_VARARGS, "feeds vertex user data. (sO|i)"}, //args=name, data, (optional) flags

	//all buffer binding calls will keep a reference to the object passed in, until after the handler has exited.
	//each bind function also accepts None for the first bytes parameter, to indicate that the buffer type should be unbound.
	{"rpgBindPositionBuffer", RPGBindPositionBuffer, METH_VARARGS, "binds position buffer. (Oii)"}, //args=bytes for positions, dataType, stride
	{"rpgBindNormalBuffer", RPGBindNormalBuffer, METH_VARARGS, "binds normal buffer. (Oii)"}, //args=bytes for normals, dataType, stride
	{"rpgBindTangentBuffer", RPGBindTangentBuffer, METH_VARARGS, "binds tangent buffer. (Oii)"}, //args=bytes for tangents, dataType, stride
	{"rpgBindUV1Buffer", RPGBindUV1Buffer, METH_VARARGS, "binds uv1 buffer. (Oii)"}, //args=bytes for uv1's, dataType, stride
	{"rpgBindUV2Buffer", RPGBindUV2Buffer, METH_VARARGS, "binds uv2 buffer. (Oii)"}, //args=bytes for uv2's, dataType, stride
	{"rpgBindUVXBuffer", RPGBindUVXBuffer, METH_VARARGS, "binds uvx buffer. (Oiiii)"}, //args=bytes for uv2's, dataType, stride, uv index, uv elem count
	{"rpgBindColorBuffer", RPGBindColorBuffer, METH_VARARGS, "binds color buffer. (Oiii)"}, //args=bytes for colors, dataType, stride, num colors (3=rgb, 4=rgba)
	{"rpgBindBoneIndexBuffer", RPGBindBoneIndexBuffer, METH_VARARGS, "binds bone index buffer. (Oiii)"}, //args=bytes for bone indices, dataType, stride, number of indices per vert
	{"rpgBindBoneWeightBuffer", RPGBindBoneWeightBuffer, METH_VARARGS, "binds bone weight buffer. (Oiii)"}, //args=bytes for bone weights, dataType, stride, number of weights per vert
	{"rpgFeedMorphTargetPositions", RPGFeedMorphTargetPositions, METH_VARARGS, "feed vmorph position buffer. (Oii)"}, //args=bytes for positions, dataType, stride
	{"rpgFeedMorphTargetNormals", RPGFeedMorphTargetNormals, METH_VARARGS, "feed vmorph normal buffer. (Oii)"}, //args=bytes for positions, dataType, stride
	{"rpgCommitMorphFrame", RPGCommitMorphFrame, METH_VARARGS, "commits a frame of bound vertex morph data. (i)"}, //args=numverts for the morph frame
	{"rpgCommitMorphFrameSet", RPGCommitMorphFrameSet, METH_NOARGS, "commits all frames of bound vertex morph data."}, //args=none
	{"rpgGetMorphBase", RPGGetMorphBase, METH_NOARGS, "returns current morph frame base index."}, //args=none
	{"rpgSetMorphBase", RPGSetMorphBase, METH_VARARGS, "sets current morph frame base index. (i)"}, //args=morph frame base index, use -1 to invalidate current base
	{"rpgClearBufferBinds", RPGClearBufferBinds, METH_NOARGS, "clears all bound buffers."}, //args=none
	{"rpgCommitTriangles", RPGCommitTriangles, METH_VARARGS, "commit triangle buffer as bytes. (Oiii|i)"}, //args=bytes for index buffer, dataType, numIdx, primType, usePlotMap (1 or 0)
	{"rpgBindUserDataBuffer", RPGBindUserDataBuffer, METH_VARARGS, "binds user data buffer. (sOii|i)"}, //args=name, data bytes, element size, stride (may be 0 to specify per-instance instead of per-vertex), (optional) offset

	//versions of the bind functions that take a direct offset
	{"rpgBindPositionBufferOfs", RPGBindPositionBufferOfs, METH_VARARGS, "binds position buffer. (Oiii)"}, //args=bytes for positions, dataType, stride, offset
	{"rpgBindNormalBufferOfs", RPGBindNormalBufferOfs, METH_VARARGS, "binds normal buffer. (Oiii)"}, //args=bytes for normals, dataType, stride, offset
	{"rpgBindTangentBufferOfs", RPGBindTangentBufferOfs, METH_VARARGS, "binds tangent buffer. (Oiii)"}, //args=bytes for tangents, dataType, stride, offset
	{"rpgBindUV1BufferOfs", RPGBindUV1BufferOfs, METH_VARARGS, "binds uv1 buffer. (Oiii)"}, //args=bytes for uv1's, dataType, stride, offset
	{"rpgBindUV2BufferOfs", RPGBindUV2BufferOfs, METH_VARARGS, "binds uv2 buffer. (Oiii)"}, //args=bytes for uv2's, dataType, stride, offset
	{"rpgBindUVXBufferOfs", RPGBindUVXBufferOfs, METH_VARARGS, "binds uvx buffer. (Oiiiii)"}, //args=bytes for uv2's, dataType, stride, uv index, uv elem count, offset
	{"rpgBindColorBufferOfs", RPGBindColorBufferOfs, METH_VARARGS, "binds color buffer. (Oiiii)"}, //args=bytes for colors, dataType, stride, offset, num colors (3=rgb, 4=rgba)
	{"rpgBindBoneIndexBufferOfs", RPGBindBoneIndexBufferOfs, METH_VARARGS, "binds bone index buffer. (Oiiii)"}, //args=bytes for bone indices, dataType, stride, offset, number of indices per vert
	{"rpgBindBoneWeightBufferOfs", RPGBindBoneWeightBufferOfs, METH_VARARGS, "binds bone weight buffer. (Oiiii)"}, //args=bytes for bone weights, dataType, stride, offset, number of weights per vert
	{"rpgFeedMorphTargetPositionsOfs", RPGFeedMorphTargetPositionsOfs, METH_VARARGS, "feed vmorph position buffer. (Oiii)"}, //args=bytes for positions, dataType, stride, offset
	{"rpgFeedMorphTargetNormalsOfs", RPGFeedMorphTargetNormalsOfs, METH_VARARGS, "feed vmorph normal buffer. (Oiii)"}, //args=bytes for positions, dataType, stride, offset

	{"rpgOptimize", RPGOptimize, METH_NOARGS, "optimizes lists to remove duplicate vertices, sorts triangles by material, etc."}, //args=none
	{"rpgSmoothNormals", RPGSmoothNormals, METH_NOARGS, "generates smoothed normals."}, //args=none
	{"rpgFlatNormals", RPGFlatNormals, METH_NOARGS, "generates flat normals."}, //args=none
	{"rpgSmoothTangents", RPGSmoothTangents, METH_NOARGS, "generates smoothed tangents."}, //args=none
	{"rpgUnifyBinormals", RPGUnifyBinormals, METH_VARARGS, "unifies tangent binormals. (i)"}, //args=flip (flips binormals if 1)
	{"rpgCreatePlaneSpaceUVs", RPGCreatePlaneSpaceUVs, METH_NOARGS, "generates plane-space uv's."}, //args=none
	{"rpgSkinPreconstructedVertsToBones", RPGSkinPreconstructedVertsToBones, METH_VARARGS, "skins all relevant committed (via immEnd/rpgCommitTriangles) vertex components using the provided bone list. must be performed prior to rpgConstructModel. (O|ii)"}, //args=bone list, (optional) vertex start index, (optional) vertex count
	{"rpgGetVertexCount", RPGGetVertexCount, METH_NOARGS, "returns number of vertices for current rpgeo context."}, //args=none
	{"rpgGetTriangleCount", RPGGetTriangleCount, METH_NOARGS, "returns number of triangles for current rpgeo context."}, //args=none
	{"rpgConstructModel", RPGConstructModel, METH_NOARGS, "returns a NoeModel constructed from the rpgeo."}, //args=none
	{"rpgConstructModelSlim", RPGConstructModelSlim, METH_NOARGS, "same as rpgConstructModel but omits various data types."}, //args=none
	{"rpgConstructModelAndSort", RPGConstructModelAndSort, METH_NOARGS, "returns a NoeModel constructed from the rpgeo."}, //args=none
	{"rpgConstructModelAndSortSlim", RPGConstructModelAndSortSlim, METH_NOARGS, "same as rpgConstructModelAndSort but omits various data types."}, //args=none
