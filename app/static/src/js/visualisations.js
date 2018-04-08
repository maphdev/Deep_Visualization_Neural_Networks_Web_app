/*
Copyright 2018 (C) A. Brabant A. Delasalle L. Leduc M. Philippot

This file is part of P&P Deep-Vis.

P&P Deep-Vis is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

P&P Deep-Vis is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

# You should have received a copy of the GNU Lesser General Public License along
# with P&P Deep-Vis; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

function changeVisuForm(evt, visuName) {
  var i, x, tablinks;
  x = document.getElementsByClassName("visu");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(visuName).style.display = "block";
  evt.currentTarget.className += " active";
}
$("#reason-checkbox").click(function() {
  $("#reason-layer").attr("disabled", this.checked);
  $("#reason-unit").attr("disabled", this.checked);
});
