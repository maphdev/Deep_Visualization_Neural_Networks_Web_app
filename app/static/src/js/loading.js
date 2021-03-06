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

function showLoading(){
  document.getElementById("loading").style = "visibility: visible";
}
function hideLoading(){
  document.getElementById("loading").style = "visibility: hidden";
}
$("#upload").change(function () {
  showLoading();
  $.ajax({
      type: "POST",
      url: "upload.php",
      enctype: 'multipart/form-data',
      data: {
          file: myfile
      },
      success: function () {
          hideLoading();
      },
      error  : function (a) {
          hideLoading();
      }
  });
});
