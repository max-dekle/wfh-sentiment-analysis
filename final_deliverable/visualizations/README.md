# Visualizations
## Yearly Sentiment Bar Graph
- **Why did you pick this representation?**
It ultimately came down to a bar graph or a line graph.  This representation lent itself nicely to the few x values of this plot.  Since there are only 4 years in question, a line graph felt like overkill; the progression from year to year is easy to see in the bars, and the values are easier to compare among sources.  Further, the linear interpolation would have been pronounced in a line graph.  These being yearly means, the histogram representation conveys only the information that we know without suggesting intermediate values that are not accurate or germane.
- **What alternative ways might you communicate the result?**
This could hypothetically have also been a line graph, but was not for the reasons mentioned.  I could have used a scatter plot, but it seemed that would have made the specific values unclear.  The data is also too sparse for a scatter plot.  I could have used a box plot to convey some more statistical information about the yearly sentiments, but this would have become a bit too dense when comparing the multiple sources each year.
- **Were there any challenges visualizing the results, if so, what where they?**
The biggest challenge was deciding how to best compare the sentiments from various sources, making both change over time and internal difference clear.  This pushed me away from using a line for this representation and towards a staggered histogram, which keeps the information neat and legible.
- **Will your visualization require text to provide context or is it standalone (either is fine, but it’s recognized which type your visualization is)?**
With knowledge of what we did for the project, it is standalone.
## Monthly Sentiment Line Graph
- **Why did you pick this representation?**
Once again, the final decision came down to a bar graph or a line graph.  Because there is much more temporal information included in this graph, with many more points on the x axis, I decided it should be a line.  This makes the progression over time clearer and the graph as a whole more clean and readable.  I also knew I wanted to include a rolling mean, which I knew would be a line graph, so I thought it would be most beneficial that they be of the same style.
- **What alternative ways might you communicate the result?**
This could also have been a bar graph, but the focus of this graph is much more on the small scale temporal evolution of the data, so that would have obscured its purpose.  It also would have been more awkward, as a bar graph with a million bars is difficult to parse.  The scatter plot would have been more applicable here but the data is so erratic that it would have failed to really convey anything.  The box plot was not even really a consideration, the information would have been way too dense.
- **Were there any challenges visualizing the results, if so, what where they?**
The challenge here was avoiding an overly cluttered graph, which ultimately led me to the line representation on a relatively large figure.  The sentiments are quite erratic and I wanted this to be clear while not too visually offensive.  Ultimately, this lack of trend and high variance was the biggest obstacle here.
- **Will your visualization require text to provide context or is it standalone (either is fine, but it’s recognized which type your visualization is)?**
Once again this is standalone with prior knowledge of the project.
## Rolling 3-month Sentiment Line Graph
- **Why did you pick this representation?**
This was an easy decision.  I wanted to include a rolling mean to expand on the information provided by the monthly average graph, as well as the raw data for the opportunity display its 'all-over-the-place-ness'.  It was valuable for its display of the high variance characterizing the underlying data while showing via the rolling mean that the overall trend was relatively unremarkable.
- **What alternative ways might you communicate the result?**
Rolling means are traditionally conveyed this way, and with good reason.  A scatter plot could have potentially been used, but it would have been difficult to read and a generally unusual choice.  Aside from that, there are not too many obvious options.
- **Were there any challenges visualizing the results, if so, what where they?**
This data was the easiest to pick a representation for, as rolling means are traditionally displayed in this particular way.  The wild nature of the raw data makes it somewhat resistant to clear visualizations, but this is less an issue on the visualization side and more an issue on the data side.  That is to say, conveying how crazy the data is was a goal and not something to try to conceal.
- **Will your visualization require text to provide context or is it standalone (either is fine, but it’s recognized which type your visualization is)?**
With prior knowledge of the project and also what a rolling mean is, this is standalone as well.
