# Microsoft Developer Studio Project File - Name="Estimacao" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 6.00
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Console Application" 0x0103

CFG=Estimacao - Win32 Debug
!MESSAGE This is not a valid makefile. To build this project using NMAKE,
!MESSAGE use the Export Makefile command and run
!MESSAGE 
!MESSAGE NMAKE /f "Estimacao.mak".
!MESSAGE 
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "Estimacao.mak" CFG="Estimacao - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "Estimacao - Win32 Release" (based on "Win32 (x86) Console Application")
!MESSAGE "Estimacao - Win32 Debug" (based on "Win32 (x86) Console Application")
!MESSAGE 

# Begin Project
# PROP AllowPerConfigDependencies 0
# PROP Scc_ProjName ""
# PROP Scc_LocalPath ""
CPP=cl.exe
F90=df.exe
RSC=rc.exe

!IF  "$(CFG)" == "Estimacao - Win32 Release"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 0
# PROP BASE Output_Dir "Release"
# PROP BASE Intermediate_Dir "Release"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 0
# PROP Output_Dir "Release"
# PROP Intermediate_Dir "Release"
# PROP Target_Dir ""
# ADD BASE F90 /compile_only /nologo /warn:nofileopt
# ADD F90 /compile_only /nologo /warn:nofileopt
# ADD BASE CPP /nologo /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /c
# ADD CPP /nologo /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /c
# ADD BASE RSC /l 0x416 /d "NDEBUG"
# ADD RSC /l 0x416 /d "NDEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib /nologo /subsystem:console /machine:I386
# ADD LINK32 kernel32.lib /nologo /subsystem:console /machine:I386

!ELSEIF  "$(CFG)" == "Estimacao - Win32 Debug"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 1
# PROP BASE Output_Dir "Debug"
# PROP BASE Intermediate_Dir "Debug"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 1
# PROP Output_Dir "Debug"
# PROP Intermediate_Dir "Debug"
# PROP Target_Dir ""
# ADD BASE F90 /check:bounds /compile_only /dbglibs /debug:full /nologo /traceback /warn:argument_checking /warn:nofileopt
# ADD F90 /check:bounds /compile_only /dbglibs /debug:full /nologo /traceback /warn:argument_checking /warn:nofileopt
# ADD BASE CPP /nologo /W3 /Gm /GX /ZI /Od /D "WIN32" /D "_DEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /GZ /c
# ADD CPP /nologo /W3 /Gm /GX /ZI /Od /D "WIN32" /D "_DEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /GZ /c
# ADD BASE RSC /l 0x416 /d "_DEBUG"
# ADD RSC /l 0x416 /d "_DEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib /nologo /subsystem:console /debug /machine:I386 /pdbtype:sept
# ADD LINK32 kernel32.lib /nologo /subsystem:console /incremental:no /debug /machine:I386 /pdbtype:sept

!ENDIF 

# Begin Target

# Name "Estimacao - Win32 Release"
# Name "Estimacao - Win32 Debug"
# Begin Group "Arquivos do Enxame_Maxima"

# PROP Default_Filter "cpp;c;cxx;rc;def;r;odl;idl;hpj;bat;f90;for;f;fpp"
# Begin Source File

SOURCE=.\Calcula.f90
DEP_F90_CALCU=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Derivadas.f90
DEP_F90_DERIV=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Enxame0.f90
DEP_F90_ENXAM=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Enxame1.f90
DEP_F90_ENXAME=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Enxame2.f90
DEP_F90_ENXAME2=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Flagmodelo.f90
# End Source File
# Begin Source File

SOURCE=.\Inversa.f90
# End Source File
# Begin Source File

SOURCE=.\Principal.f90
DEP_F90_PRINC=\
	{$(INCLUDE)}"IMSL.mod"\
	
NODEP_F90_PRINC=\
	".\Debug\CALLIMOD.MOD"\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Regres0.f90
DEP_F90_REGRE=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Regres1.f90
DEP_F90_REGRES=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Regres2.f90
NODEP_F90_REGRES2=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Variaveis.f90
# End Source File
# End Group
# Begin Group "Arquivos do Usuario"

# PROP Default_Filter "h;hpp;hxx;hm;inl;fi;fd"
# Begin Group "Ddaspk"

# PROP Default_Filter ""
# Begin Source File

SOURCE=.\Ddaspk\daux.f
# End Source File
# Begin Source File

SOURCE=.\Ddaspk\ddaspk.f
# End Source File
# Begin Source File

SOURCE=.\Ddaspk\dlinpk.f
# End Source File
# End Group
# Begin Source File

SOURCE=.\dadosbusca.dat
# End Source File
# Begin Source File

SOURCE=.\dadosexp.dat
# End Source File
# Begin Source File

SOURCE=.\Leitura.f90
NODEP_F90_LEITU=\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Modelo.f90
NODEP_F90_MODEL=\
	".\Debug\CALLIMOD.MOD"\
	".\Debug\Variaveis.mod"\
	
# End Source File
# Begin Source File

SOURCE=.\Taxa.f90
NODEP_F90_TAXA_=\
	".\Debug\CALLIMOD.MOD"\
	".\Debug\Variaveis.mod"\
	
# End Source File
# End Group
# Begin Group "Resultados"

# PROP Default_Filter "ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe"
# Begin Source File

SOURCE=.\avaliacao.dat
# End Source File
# Begin Source File

SOURCE=.\grafico.dat
# End Source File
# Begin Source File

SOURCE=.\RegConf.dat
# End Source File
# Begin Source File

SOURCE=.\relatorio.dat
# End Source File
# Begin Source File

SOURCE=.\saida.dat
# End Source File
# Begin Source File

SOURCE=.\Saida_bom.dat
# End Source File
# Begin Source File

SOURCE=.\Saida_tudo.dat
# End Source File
# End Group
# End Target
# End Project
