Attribute VB_Name = "pySABR_web"
Option Explicit
Option Base 1

Public Function pySABR_alpha(ATM_vol As Double, f As Double, t As Double, Beta As Double, Rho As Double, Vovol As Double)
    
    Dim pySABR_service As String
    Dim result As Double
    pySABR_service = "http://127.0.0.1:5000/alpha?atm=" & ATM_vol & "&f=" & f & "&t=" & t & "&b=" & Beta & "&r=" & Rho & "&n=" & Vovol
    result = WorksheetFunction.WebService(SABR_service_url)
    LogNormal_SABR_Alpha_Web = result
    
End Function

Public Function pySABR_lognormal_vol(k As Double, f As Double, t As Double, Alpha As Double, Beta As Double, Rho As Double, Vovol As Double)
    
    Dim pySABR_service As String
    Dim result As Double
    pySABR_service = "http://127.0.0.1:5000/sabr?k=" & k & "&f=" & f & "&t=" & t & "&a=" & Alpha & "&b=" & Beta & "&r=" & Rho & "&n=" & Vovol
    result = WorksheetFunction.WebService(SABR_service_url)
    LogNormal_SABR_Web = result * 100
    
End Function
