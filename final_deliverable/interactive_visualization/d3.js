let articleData = []
let currData = []
fetch('combined_ratings_and_articles.json')
    .then(response => response.json())
    .then(data => {
        articleData = data;
        // Do something with the articleData, for example:
        currData = articleData
        plot()

    })
    .catch(error => {
        console.error('Error:', error);
    });

let sourceColors = {
    "The Guardian": "#7f7f7f",
    "New York Times": "#8c564b",
    "Reddit /r/experienceddevs": "#1f77b4",
    "Reddit /r/cscareerquestions": "#ff7f0e"}



function plot() {
    //
    // let width = 1000, height = 400;
    //
    // let zoom = d3.zoom()
    //     .scaleExtent([1, 5])
    //     .translateExtent([[0, 0], [width, height]])
    //     .on('zoom', handleZoom);
    // function handleZoom(e) {
    //     d3.select('svg g')
    //         .attr('transform', e.transform);
    // }
    //
    // function initZoom() {
    //     d3.select('svg')
    //         .call(zoom);
    // }
    //
    // initZoom();

    let svg = d3.select("#plotSVG")
        .style("overflow","visible") // some tooltips stray outside the SVG border
        .append("g")
        .attr("transform", "translate(50,50)")

    // y axis
    let yScale = d3.scaleLinear()
        .domain([-1.0, 1.0])   // my y-variable has a max of 1200
        .range([400, 0]);   // my y-axis is 400px high
                            // (the max and min are reversed because the
                            // SVG y-value is measured from the top)
    svg.append("g")       // the axis will be contained in an SVG group element
        .attr("id","yAxis")
        .call(d3.axisLeft(yScale)
            .ticks(10)
            .tickFormat(d3.format(".1f"))  // format to one decimal place
            .tickSizeOuter(0)
        )

    // x axis
    let xScale = d3.scaleBand()
        .domain(Object.keys(sourceColors))
        .range([0, 1000])
        .padding(1) // space them out so the bubble appears in the centre

    svg.append("g")
        .attr("transform", "translate(0,400)")    // translate x-axis to bottom of chart
        .attr("id","xAxis")
        .call(d3.axisBottom(xScale).tickSize(0))
        .selectAll("text")
        // offset the publication names to fit them in horizontally
        .attr("transform", (d,i)=>`translate(0, ${(i%2)*20})`)
        .style("fill", d => sourceColors[d])


    svg.append("text")
        .attr("x", 500)
        .attr("y", -70)
        .attr("text-anchor", "middle")
        .style("font-size", "24px")
        .style("font-family", "sans-serif")
        .text("Sentiment Ratings of Online Sources from 2020 to 2023");


    let xVar = document.getElementById("select-x-var").value;

    if(xVar === "DATE") {
        xScale = d3.scaleTime()
            .domain([d3.min(currData, d => d[xVar]), d3.max(currData, d => d[xVar])])
            .range([0, 1000]);

        d3.select("#xAxis")
            .call(d3.axisBottom(xScale)
                .tickFormat(d3.timeFormat("%b %d %y")))
        //see here for time formatting options:
        // https://github.com/d3/d3-time-format

        // transition each circle element
        svg.selectAll(".bubble")
            .transition()
            .duration(1000)
            .attr("cx", (d) => xScale(d[xVar]) )


        // bubbles
        svg.selectAll(".bubble")
            .data(currData)    // bind each element of the data array to one SVG circle
            .join("circle")
            .attr("class", "bubble")
            .attr("cx", d => xScale(d.DATE))   // set the x position based on the number of claps
            .attr("cy", d => yScale(d.RATING))   // set the y position based on the number of views
            .attr("r", 2)  // set the radius based on the article reading time
            .attr("stroke", d => sourceColors[d.SOURCE])
            .attr("fill", d => sourceColors[d.SOURCE])
            .attr("fill-opacity", 0.5)
            .on("mouseover",(e,d) => {    // event listener to show tooltip on hover
                d3.select("#bubble-tip-"+d.index)  // i'm using the publish time as a unique ID
                    .style("display","block");
            })
            .on("mouseout", (e,d) => {    // event listener to hide tooltip after hover
                if(!d.toolTipVisible){
                    d3.select("#bubble-tip-"+d.index)
                        .style("display","none");
                }
            })
            .on("click", (e,d) => {    // event listener to make tooltip remain visible on click
                if(!d.toolTipVisible){
                    d3.select("#bubble-tip-"+d.index)
                        .style("display", "block");
                    d.toolTipVisible = true;
                }
                else{
                    d3.select("#bubble-tip-"+d.index)
                        .style("display", "none");
                    d.toolTipVisible = false;
                }
            });

        svg.selectAll(".bubble-tip")
            .data(currData)
            .join("g")
            .attr("class", "bubble-tip")
            .attr("id", (d)=> "bubble-tip-"+d.index)
            .attr("transform", d => "translate(" + (xScale(d.DATE)+20) + ", " + yScale( d.RATING) + ")"  )
            .style("display", "none")
            .append("rect")     // this is the background to the tooltip
            .attr("x",-5)
            .attr("y",-20)
            .attr("rx",5)
            .attr("fill",d => sourceColors[d.SOURCE])
            .attr("fill-opacity", 0.9)
            .attr("width",300)
            .attr("height",40)

        // Append x axis title

        setXAxisTitle("")
        setXAxisTitle("Date")

    } else {
        // bubbles
        svg.selectAll(".bubble")
            .data(currData)    // bind each element of the data array to one SVG circle
            .join("circle")
            .attr("class", "bubble")
            .attr("cx", d => xScale(d.SOURCE))   // set the x position based on the number of claps
            .attr("cy", d => yScale(d.RATING))   // set the y position based on the number of views
            .attr("r", 2)  // set the radius based on the article reading time
            .attr("stroke", d => sourceColors[d.SOURCE])
            .attr("fill", d => sourceColors[d.SOURCE])
            .attr("fill-opacity", 0.5)
            .on("mouseover",(e,d) => {    // event listener to show tooltip on hover
            d3.select("#bubble-tip-"+d.index)  // i'm using the publish time as a unique ID
                .style("display","block");
            })
            .on("mouseout", (e,d) => {    // event listener to hide tooltip after hover
                if(!d.toolTipVisible){
                    d3.select("#bubble-tip-"+d.index)
                        .style("display","none");
                }
            })
            .on("click", (e,d) => {    // event listener to make tooltip remain visible on click
                if(!d.toolTipVisible){
                    d3.select("#bubble-tip-"+d.index)
                        .style("display", "block");
                    d.toolTipVisible = true;
                }
                else{
                    d3.select("#bubble-tip-"+d.index)
                        .style("display", "none");
                    d.toolTipVisible = false;
                }
            });

        svg.selectAll(".bubble-tip")
            .data(currData)
            .join("g")
            .attr("class", "bubble-tip")
            .attr("id", (d)=> "bubble-tip-"+d.index)
            .attr("transform", d => "translate(" + (xScale( d.SOURCE )+20) + ", " + yScale( d.RATING) + ")"  )
            .style("display", "none")
            .append("rect")     // this is the background to the tooltip
            .attr("x",-5)
            .attr("y",-20)
            .attr("rx",5)
            .attr("fill",d => sourceColors[d.SOURCE])
            .attr("fill-opacity", 0.9)
            .attr("width",300)
            .attr("height",40)


        // Append x axis title

        setXAxisTitle("")
        setXAxisTitle("Source")

    }

// SVG does not wrap text
// so I add a new text element for each line (4 words)
    svg.selectAll(".bubble-tip")
        .append("text")
        .append("a")
        .attr("href", d => d.URL)
        .attr("target", "_blank") // to open the link in a new tab
        .text(d =>d.URL.split("").slice(0,41).join("") + "...")
        .style("font-family", "sans-serif")
        .style("font-size", 14)
        .attr("stroke", "none")
        .attr("fill", "white")



// Append y axis title
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - 80)
        .attr("x",0 - (400 / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .style("font-family", "sans-serif")
        .style("font-size", 17)
        .text("Sentiment Ratings");




    document.getElementById("select-source").addEventListener("change", (e)=>{
        let sourceVar = e.target.value

        if(sourceVar==='All'){
            currData = articleData;

        } else {
            console.log(sourceVar)
            currData = articleData.filter(item => item.SOURCE === sourceVar)

        }
        d3.select("#plotSVG g").remove();
        plot()

    })

    document.getElementById("select-x-var").addEventListener("change", (e)=>{

        // update the x-variable based on the user selection
        xVar = e.target.value

        if(xVar === "DATE"){
            xScale = d3.scaleTime()
                .domain([d3.min(currData, d => d[xVar]), d3.max(currData, d => d[xVar])])
                .range([0, 1000]);

            d3.select("#xAxis")
                .call(d3.axisBottom(xScale)
                    .tickFormat(d3.timeFormat("%b %d %y")) )
            //see here for time formatting options:
            // https://github.com/d3/d3-time-format

            svg.selectAll(".bubble-tip")
                .attr("transform", d => "translate(" + (xScale( d.DATE )+20) + ", " + yScale( d.RATING) + ")"  )


            setXAxisTitle("")
            setXAxisTitle("Date")
        } else{
            xScale = d3.scaleBand()
                .domain(Object.keys(sourceColors))
                .range([0, 1000])
                .padding(1) // space them out so the bubble appears in the centre

            svg.select("#xAxis")
                .call(d3.axisBottom(xScale).tickSize(0))
                .selectAll("text")
                // offset the publication names to fit them in horizontally
                .attr("transform", (d,i)=>`translate(0, ${(i%2)*20})`)
                .style("fill", d => sourceColors[d])


            svg.selectAll(".bubble-tip")
                .attr("transform", d => "translate(" + (xScale( d.SOURCE )+20) + ", " + yScale( d.RATING) + ")"  )


            // Append x axis title
            setXAxisTitle("")
            setXAxisTitle("Source")
        }
        // transition each circle element
        svg.selectAll(".bubble")
            .transition()
            .duration(1000)
            .attr("cx", (d) => xScale(d[xVar]) )
    })

    function setXAxisTitle(text) {
        svg.select("#title").remove();  // remove any existing title
        svg.append("text")
            .attr("id", "title")
            .attr("transform", "translate(" + (1000/2) + " ," + (400 + 60 + 20) + ")")
            .style("text-anchor", "middle")
            .style("font-size", 17)
            .style("font-family", "sans-serif")
            .text(text);
    }

}
