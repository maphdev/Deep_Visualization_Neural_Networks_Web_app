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

function importData (filename) {
  var tab = new Array;

  var color = d3.scale.category20();

  d3.json(filename, function(error, graph) {
      var nodes = graph;
      console.log(graph);

      for (var i = 0; i< nodes.length; i++){
        tab[i]= nodes[i].class_name;
        createD3Rect(i);
        testD3Graph();
      }

      $(".layer").attr("max", nodes.length-1);
      $(".layer").val(nodes.length-1);
      $("#reason-checkbox").click(function() {
        $(".layer").val(nodes.length-1);
      });

      function createD3Rect(i){

        var svgContainer = d3.select(".dataContainer").append("svg")
                                       .attr("width", 200)
                                       .attr("height", 60);

        //Draw the Rectangle
        var rectangle = svgContainer.append("rect")
                                    .attr("x", 0)
                                    .attr("y", 0)
                                    .attr("rx",10)
                                    .attr("ry", 10)
                                    .attr("width", 150)
                                    .attr("height", 45)
                                    .attr("title", "Nom du layer : "+ nodes[i].name + " Shape : " + nodes[i].shape)
                                    .attr("fill", getLayerColor(tab[i]))
                                    .attr("stroke", "DeepSkyBlue")
                                    .attr("stroke-width", 0)
                                    .on("mouseover",
                                    function(d){d3.select(this).attr("fill", "DeepSkyBlue");})
                                    .on("mouseout",
                                    function(d){d3.select(this).attr("fill", getLayerColor(tab[i]));})
                                    .on("click",function(){$(".layer").val(i);});
        //rectangle.on("onmouseenter", rectangle.attr("stroke","AliceBlue "));

        var text = svgContainer.append("text")
                              .attr("x", 25)
                              .attr("y", 30)
                              .on("click",function(){$(".layer").val(i);})
                              .text(tab[i]);
        if (i != (nodes.length)-1) {
          var arrow = svgContainer.append("line").attr("x1", 75)
                                                    .attr("y1", 45)
                                                    .attr("x2", 75)
                                                    .attr("y2", 60)
                                                    .attr("x",35)
                                                    .attr("y",75)
                                                    .attr("stroke-width", 2)
                                                    .attr("stroke", "black");
        }
      }
      function getLayerColor(LayerName){
        switch (LayerName){
          case "InputLayer":
            return "LimeGreen";
          case "Conv2D":
            return "MediumTurquoise ";
          case "Dense":
            return "LightSalmon";
          case "MaxPooling2D":
            return "MediumPurple ";
          case "Flatten":
            return "Cornsilk ";
        }
        return "lightGrey";
      }

      function testD3Graph(){
        var b = d3.selectAll("rect");
        if (b.length = nodes.length)
          console.log("test passé");
        else
          console.log("le nombre de rectangle d3 créés n'est pas egual au nombre de layers du reaseau de neurone.")
      }
  });
}
