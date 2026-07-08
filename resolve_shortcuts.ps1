# Script pour remplacer les raccourcis Windows (.lnk) par les fichiers cibles réels
$sh = New-Object -ComObject WScript.Shell
$scriptFolder = Split-Path -Parent $MyInvocation.MyCommand.Definition
$programmesFolder = Join-Path $scriptFolder "programmes"

if (Test-Path $programmesFolder) {
    Get-ChildItem -Path $programmesFolder -Filter *.lnk | ForEach-Object {
        $lnkPath = $_.FullName
        try {
            $shortcut = $sh.CreateShortcut($lnkPath)
            $targetPath = $shortcut.TargetPath
            
            if ($targetPath -and (Test-Path $targetPath)) {
                $destinationName = $_.Name.Substring(0, $_.Name.Length - 4) # Enlever le .lnk
                $destinationPath = Join-Path $programmesFolder $destinationName
                
                Write-Host "Résolution du raccourci : $_.Name -> $targetPath"
                Write-Host "Copie du fichier physique vers : $destinationPath"
                
                # Copier le fichier réel
                Copy-Item -Path $targetPath -Destination $destinationPath -Force
                
                # Supprimer le fichier .lnk pour qu'il ne soit pas committé
                Remove-Item -Path $lnkPath -Force
                
                # Ajouter la modification à Git
                git rm --cached -f "$lnkPath" 2>$null
                git add "$destinationPath"
            } else {
                Write-Warning "Cible introuvable ou invalide pour le raccourci: $_.Name ($targetPath)"
            }
        } catch {
            Write-Error "Erreur lors du traitement de $_.Name : $_"
        }
    }
}
