Instructions
Check the Material Symbols guide for advanced examples such as animations and font loading optimization.

Variable icon font
Add the variable font stylesheet request to your head tag and the current variable axes configuration to icons using CSS.

<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=paid" />
<style>
.material-symbols-outlined {
  font-variation-settings:
  'FILL' 0,
  'wght' 400,
  'GRAD' 0,
  'opsz' 24
}
</style>
Static icon font
Alternatively, the current configuration can be loaded as a static font instead of a variable one.

<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=paid" />
Inserting the icon
<span class="material-symbols-outlined">
paid
</span>
Code point
f041
Icon name
paid
