Attribute VB_Name = "pySABR_web"
Option Explicit
Option Base 1

Public Const pySABR_host As String = "us051vm:5000"
' Public Const pySABR_host = "127.0.0.1:5000" --> localhost for dev

Public Function pySABR_alpha(ATM_vol As Double, f As Double, t As Double, Beta As Double, Rho As Double, Vovol As Double)

    Dim pySABR_service As String
    Dim result As Double
    pySABR_service = "http://" & pySABR_host & "/alpha?v=" & ATM_vol & "&f=" & f & "&t=" & t & "&b=" & Beta & "&r=" & Rho & "&n=" & Vovol
    result = WorksheetFunction.WebService(pySABR_service)
    pySABR_alpha = result

End Function

Public Function pySABR_lognormal_vol(k As Double, f As Double, t As Double, Alpha As Double, Beta As Double, Rho As Double, Vovol As Double)

    Dim pySABR_service As String
    Dim result As Double
    pySABR_service = "http://" & pySABR_host & "/sabr?k=" & k & "&f=" & f & "&t=" & t & "&a=" & Alpha & "&b=" & Beta & "&r=" & Rho & "&n=" & Vovol
    result = WorksheetFunction.WebService(pySABR_service)
    pySABR_lognormal_vol = result

End Function
