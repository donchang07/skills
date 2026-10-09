[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$Source,[Parameter(Mandatory=$true)][string]$Output,[Parameter(Mandatory=$true)][string]$Contract,[string]$RenderDir)
$ErrorActionPreference='Stop'
function V($o,$k,$d){if($null -ne $o -and $null -ne $o.$k){[double]$o.$k}else{[double]$d}}
function Managed($n){$n -like 'Story explanation*' -or $n -eq 'Story headline' -or $n -eq 'Story detail' -or $n.StartsWith('ChangPPT narrative ')}
function Box($s,$name,$text,$x,$w,$bold,$wrap){
 $b=$s.Shapes.AddTextbox(1,[single]$x,0,[single]$w,20);$b.Name=$name;$b.Fill.Visible=0;$b.Line.Visible=0
 $f=$b.TextFrame;$f.AutoSize=0;$f.WordWrap=$(if($wrap){-1}else{0});$f.VerticalAnchor=1
 $f.MarginLeft=0;$f.MarginRight=0;$f.MarginTop=0;$f.MarginBottom=0
 $r=$f.TextRange;$r.Text=$text;$r.Font.Name='Pretendard';$r.Font.NameFarEast='Pretendard';$r.Font.NameOther='Pretendard';$r.Font.Size=14;$r.Font.Bold=$(if($bold){-1}else{0});$r.Font.Color.RGB=5914156
 $r.ParagraphFormat.Alignment=2;$r.ParagraphFormat.SpaceWithin=1.0;$b.TextFrame2.AutoSize=0
 return $b
}
$Source=[IO.Path]::GetFullPath($Source);$Output=[IO.Path]::GetFullPath($Output);$Contract=[IO.Path]::GetFullPath($Contract)
if(!(Test-Path -LiteralPath $Source -PathType Leaf)){throw 'Source missing.'}
if($Source -eq $Output){throw 'Output must differ from Source.'}
if(Test-Path -LiteralPath $Output){throw 'Existing output refused.'}
$mp=$Output+'.metrics.json';if(Test-Path -LiteralPath $mp){throw 'Existing metrics refused.'}
if(!(Test-Path -LiteralPath ([IO.Path]::GetDirectoryName($Output)) -PathType Container)){throw 'Output parent missing.'}
if($RenderDir){$RenderDir=[IO.Path]::GetFullPath($RenderDir);if(Test-Path -LiteralPath $RenderDir){throw 'Existing render directory refused.'}}
$c=Get-Content -LiteralPath $Contract -Raw -Encoding UTF8|ConvertFrom-Json
if(!$c.slides){throw 'Contract slides required.'}
if($null -ne $c.font_size_pt -and [double]$c.font_size_pt -ne 14){throw 'Narrative font must be 14pt.'}
$hash=(Get-FileHash -LiteralPath $Source).Hash
$prior=@(Get-Process POWERPNT -ErrorAction SilentlyContinue|ForEach-Object{$_.Id})
$app=$null;$deck=$null;$own=$false;$metrics=@();$seen=@{}
try{
 $app=New-Object -ComObject PowerPoint.Application
 if(-not ('ChangPptPid' -as [type])){Add-Type 'using System; using System.Runtime.InteropServices; public static class ChangPptPid { [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint p); }'}
 [uint32]$pidValue=0;[void][ChangPptPid]::GetWindowThreadProcessId([IntPtr]$app.HWND,[ref]$pidValue)
 $own=($pidValue -ne 0 -and $pidValue -notin $prior)
 $deck=$app.Presentations.Open($Source,-1,0,0)
 $sw=[double]$deck.PageSetup.SlideWidth;$sh=[double]$deck.PageSetup.SlideHeight
 if(([Math]::Abs($sw-960) -gt 0.1 -or [Math]::Abs($sh-540) -gt 0.1) -and !$c.layout){throw 'Non-brand slide size requires explicit global layout in points.'}
 foreach($e in $c.slides){
  if($null -ne $e.slide_id){$s=$deck.Slides.FindBySlideID([int]$e.slide_id)}elseif($null -ne $e.slide_index){$s=$deck.Slides.Item([int]$e.slide_index)}else{throw 'slide_id or slide_index required.'}
  $id=[int]$s.SlideID;if($seen.ContainsKey($id)){throw "Duplicate slide $id"};$seen[$id]=$true
  if($e.role -notin @('content','toc','part','cover','profile','closing')){throw 'Invalid role.'}
  if($e.role -eq 'content' -and ([string]::IsNullOrWhiteSpace($e.headline) -or [string]::IsNullOrWhiteSpace($e.detail))){throw 'Explicit headline and detail required.'}
  if($e.role -eq 'content' -and $e.headline -match '[\r\n]'){throw 'Headline must be single line.'}
  for($i=$s.Shapes.Count;$i -ge 1;$i--){$z=$s.Shapes.Item($i);if(Managed $z.Name){$z.Delete()}}
  if($e.role -ne 'content'){$metrics+=@{slide_id=$id;slide_index=$s.SlideIndex;role=$e.role;managed_count=0};continue}
  $l=$c.layout;if($null -ne $e.layout){$l=$e.layout}
  $x=V $l 'x' 46.8;$y=V $l 'y' 410;$w=V $l 'width' ($sw-93.6);$h=V $l 'height' 78;$gap=V $l 'gap' 7
  if($x -lt 46.8 -or $y -lt 74.16 -or $w -le 0 -or $h -le 0 -or $gap -lt 0 -or $x+$w -gt $sw-36.24+0.1 -or $y+$h -gt $sh-51.84+0.1){throw 'Layout outside safe brand area.'}
  $head=Box $s 'ChangPPT narrative headline' ([string]$e.headline) $x $w $true $false
  $detail=Box $s 'ChangPPT narrative detail' ([string]$e.detail) $x $w $false $true
  $hh=[double]$head.TextFrame.TextRange.BoundHeight;$dh=[double]$detail.TextFrame.TextRange.BoundHeight;$hw=[double]$head.TextFrame.TextRange.BoundWidth;$dw=[double]$detail.TextFrame.TextRange.BoundWidth;$group=$hh+$gap+$dh
  if($hh -le 0 -or $dh -le 0 -or $hw -gt $w+0.5 -or $dw -gt $w+0.5 -or $group -gt $h+0.5){throw "Narrative overflow before save: $id"}
  $top=$y+($h-$group)/2;$head.Top=[single]$top;$head.Height=[single]($hh+0.1);$detail.Top=[single]($top+$hh+$gap);$detail.Height=[single]($dh+0.1)
  if($l.panel -eq $true){$p=$s.Shapes.AddShape(1,[single]$x,[single]$y,[single]$w,[single]$h);$p.Name='ChangPPT narrative panel';$p.Fill.ForeColor.RGB=16250357;$p.Line.Visible=0;$head.ZOrder(0);$detail.ZOrder(0)}
  $metrics+=@{slide_id=$id;slide_index=$s.SlideIndex;role=$e.role;headline=$e.headline;detail=$e.detail;font_size_pt=14;head_width=$hw;detail_width=$dw;available_width=$w;head_height=$hh;detail_height=$dh;top=$top;bottom=$top+$group;managed_count=$(if($l.panel -eq $true){3}else{2})}
 }
 $deck.SaveAs($Output,24)
 if($RenderDir){New-Item -ItemType Directory -Path $RenderDir|Out-Null;for($i=1;$i -le $deck.Slides.Count;$i++){$deck.Slides.Item($i).Export((Join-Path $RenderDir ('slide-{0:D3}.png' -f $i)),'PNG',1280,720)}}
 [ordered]@{source=$Source;source_sha256=$hash;output=$Output;contract=$Contract;render_dir=$RenderDir;renderer=$(if($RenderDir){'Microsoft PowerPoint COM PNG'}else{'not_run'});slide_count=$deck.Slides.Count;slides=$metrics}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $mp -Encoding UTF8
}finally{
 if($deck){try{$deck.Close()}catch{};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck)}
 if($app){if($own){try{$app.Quit()}catch{}};[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)}
 [GC]::Collect();[GC]::WaitForPendingFinalizers()
}
if((Get-FileHash -LiteralPath $Source).Hash -ne $hash){throw 'Source hash changed.'}
Write-Output $mp
