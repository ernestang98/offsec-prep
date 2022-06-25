$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()

$PDC = ($domainObj.PdcRoleOwner).Name

$SearchString = "LDAP://"

$SearchString += $PDC + "/"

$DistinguishedName = "DC=$($domainObj.Name.Replace('.', ',DC='))"

$SearchString += $DistinguishedName

$SearchString

$Searcher = New-Object System.DirectoryServices.DirectorySearcher([ADSI]$SearchString)

$objDomain = New-Object System.DirectoryServices.DirectoryEntry

$Searcher.SearchRoot = $objDomain

$Searcher.filter = "serviceprincipalname=*sql*"

$Result = $Searcher.FindAll()

Foreach ($obj in $Result)
{
	Foreach ($prop in $obj.Properties)
	{
		$prop
	}
}

<#

$Searcher.filter = "serviceprincipalname=*mail*"

$Result = $Searcher.FindAll()

Foreach ($obj in $Result)
{
	Foreach ($prop in $obj.Properties)
	{
		$prop
	}
}

<#
e.g. {MSSQLSvc/xor-app23.xor.com:1433} 
e.g. {HTTP/CorpWebServer.corp.com} 
nslookup DOMAIN:PORT (exclude the service)
#>
