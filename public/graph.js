Papa.parse("stock_data_1.csv", {
    download: true,
    header: true,
    complete: function (results) {
        const xarray = [];
        const yarray = [];
        const customdata = [];

        results.data.forEach(row => {
            xarray.push(row['Date']);
            yarray.push(parseFloat(row['Close']));
            customdata.push({
                Open: parseFloat(row['Open']).toFixed(2),
                High: parseFloat(row['High']).toFixed(2),
                Low: parseFloat(row['Low']).toFixed(2),
                Volume: parseInt(row['Volume']),
            })
        });

        //DATA ONLOAD

        const tarce1 = [{
            x: xarray,
            y: [],
            customdata: customdata,
            mode: "lines",
            type: "scatter",
            fill: "tozeroy",
            fillgradient: {
                type: 'vertical',
                colorscale: [[0, 'rgba(0,0,0,0)'], [1, 'rgba(96,0,147,1)']],
            },
            line: {
                width: 2
            },
            hovertemplate:
                'Date: %{x}<br>' +
                'Close: %{y}<br>' +
                `Open: %{customdata.Open}<br>` +
                `High: %{customdata.High}<br>` +
                `Low: %{customdata.Low}<br>` +
                `Volume: %{customdata.Volume}<br>` +
                '<extra></extra>',
        }];

        //LAYOUT ONLOAD


        const layout = {
            xaxis: {
                range: [xarray[0], xarray[xarray.length - 1]], title: {
                    text: "Date",
                    font: {
                        color: "white"
                    }
                },
                tickfont: {
                    color: "white"
                }
            },
            yaxis: {
                range: [0, Math.max(...yarray) + 20], title: {
                    text: "Prices",
                    font: {
                        color: "white"
                    }
                },
                tickfont: {
                    color: "white"
                }
            },
            colorway: ['#7834a8'],
            plot_bgcolor: "black",
            paper_bgcolor: "black",
        };

        //PLOTLING THE GRAPH AND ANIMATING IT WITH REQUEST ANIMATION FRAME


        Plotly.newPlot("myplot", tarce1, layout);
        let i = 0; let id;
        function animate() {
            if (i < xarray.length) {
                Plotly.extendTraces("myplot", {
                    x: [[xarray[i]]],
                    y: [[yarray[i]]]
                }, [0])
                i++;
                id = requestAnimationFrame(animate);
            }
        }
        animate();

        const stp = document.getElementById("stp");
        stp.addEventListener("click", func);
        function func() {
            Plotly.react("myplot", [{
                x: xarray,
                y: yarray,
                customdata: customdata,
                mode: "lines",
                type: "scatter",
                fill: "tozeroy",
                fillgradient: {
                    type: 'vertical',
                    colorscale: [[0, 'rgba(0,0,0,0)'], [1, 'rgba(96,0,147,1)']],
                },
                line: {
                    width: 2
                },
                hovertemplate:    //HOVERING TEMPLATE
                    'Date: %{x}<br>' +
                    'Close: %{y}<br>' +
                    `Open: %{customdata.Open}<br>` +
                    `High: %{customdata.High}<br>` +
                    `Low: %{customdata.Low}<br>` +
                    `Volume: %{customdata.Volume}<br>` +
                    '<extra></extra>',
            }], layout)
            cancelAnimationFrame(id);
        }
    }
});

//ONCLICK SECOND GRAPH ADDED ON THE SCREEN


const second = document.getElementById("second")
second.addEventListener("click", fus);
let i = 2;
function fus() {
    Papa.parse("stock_data_" + `${i}` + ".csv", {
        download: true,
        header: true,
        complete: function (results) {
            const xa = [];
            const ya = [];
            const customdata = [];

            results.data.forEach(row => {
                xa.push(row['Date']);
                ya.push(parseFloat(row['Close']));
                customdata.push({
                    Open: parseFloat(row['Open']).toFixed(2),
                    High: parseFloat(row['High']).toFixed(2),
                    Low: parseFloat(row['Low']).toFixed(2),
                    Volume: parseInt(row['Volume']),
                })
            });

            const tarce2 = [{
                x: xa,
                y: ya,
                customdata: customdata,
                mode: "lines",
                type: "scatter",
                line: {
                    width: 2
                },
                hovertemplate:
                    'Date: %{x}<br>' +
                    'Close: %{y}<br>' +
                    `Open: %{customdata.Open}<br>` +
                    `High: %{customdata.High}<br>` +
                    `Low: %{customdata.Low}<br>` +
                    `Volume: %{customdata.Volume}<br>` +
                    '<extra></extra>',
            }];

            Plotly.addTraces("myplot", tarce2);
            i++;
        }

    });

}

//BOILENGER BAND GRAPH
Papa.parse("stock_data_1.csv", {
    download: true,
    header: true,
    complete: function (results) {
        const xarray = [];
        const yarray = [];

        results.data.forEach(row => {
            xarray.push(row['Date']);
            yarray.push(parseFloat(row['Close']));
        });
        function calculate(yarray, period = 20, multiplier = 2) {
            const upper = [];
            const lower = [];
            const middle = [];
            for (let i = 0; i < yarray.length; i++) {
                if (i >= period - 1) {
                    const slice = yarray.slice(i - period + 1, i + 1);
                    const mean = slice.reduce((a, b) => a + b, 0) / period;
                    const sd = Math.sqrt(slice.map(val => Math.pow(val - mean, 2)).reduce((a, b) => a + b, 0) / period)
                    upper.push(mean + multiplier * sd);
                    middle.push(mean);
                    lower.push(mean - multiplier * sd);
                }
            }
            return { middle, lower, upper };
        }
        const boilenger = document.getElementById("boilenger");
        boilenger.addEventListener('click', () => {
            const { upper, lower, middle } = calculate(yarray);
            Plotly.addTraces("myplot", {
                x: xarray,
                y: upper,
                mode: "lines",
                type: "scatter",
                line: {
                    width: 3,
                    color: "blue"
                }
            })
            Plotly.addTraces("myplot", {
                x: xarray,
                y: lower,
                mode: "lines",
                type: "scatter",
                line: {
                    width: 3,
                    color: "blue"
                }
            })
            Plotly.addTraces("myplot", {
                x: xarray,
                y: middle,
                mode: "lines",
                type: "scatter",
                line: {
                    width: 3,
                    color: "blue"
                }
            })
        })
    }
})

//RSI MARK
// --------------------------------------------------------------------------------------------------------------------------------------
Papa.parse("stock_data_1.csv", {
    download: true,
    header: true,
    complete: function (results) {
        const xarray = [];
        const yarray = [];
        const customdata = [];

        results.data.forEach(row => {
            xarray.push(row['Date']);
            yarray.push(parseFloat(row['Close']));

        });
        function changes(yarray, period = 14) {
            let gain = [];
            let losses = [];
            for (let i = 1; i < yarray.length; i++) {
                let change = yarray[i] - yarray[i - 1];
                if (change > 0) {
                    gain.push(change);
                    losses.push(0);
                }
                else {
                    gain.push(0);
                    losses.push(Math.abs(change));
                }
            }
            let rsi = [];
            for (let i = period; i < yarray.length; i++) {
                const avggain = gain.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
                const avgloss = losses.slice(i - period, i).reduce((a, b) => a + b, 0) / period;

                let rs = avggain / avgloss;
                rsi.push(100 - (100 / (1 + rs)));
            }
            rsi = new Array(period).fill(null).concat(rsi);
            return rsi;
        }
        const rsii = document.getElementById("rsi");
        rsii.addEventListener('click', () => {
            const value = changes(yarray);

            const rsilayout = {
                xaxis: {
                    range: [xarray[0], xarray[xarray.length - 1]], title: {
                        text: "Date",
                        font: {
                            color: "white"
                        }
                    },
                    tickfont: {
                        color: "white"
                    }
                },
                yaxis: {
                    range: [0, 100], title: {
                        text: "Prices",
                        font: {
                            color: "white"
                        }
                    },
                    tickfont: {
                        color: "white"
                    }
                },
                colorway: ['#7834a8'],
                plot_bgcolor: "black",
                paper_bgcolor: "black",
            };
            const rsitrace = [{
                x: xarray,
                y: value,
                customdata: customdata,
                mode: "lines",
                type: "scatter",
                line: {
                    width: 2
                }
            }];
            Plotly.newPlot("rsigraph", rsitrace, rsilayout,)
            const ys = new Array(xarray.length).fill(70)
            const ysi = new Array(xarray.length).fill(30)
            Plotly.addTraces("rsigraph", {
                x: xarray,
                y: ys,
                mode: "lines",
                type: "scatter",
                name: "overbought (70)",
                line: {
                    color: "red",
                    width: 2
                }
            })
            Plotly.addTraces("rsigraph", {
                x: xarray,
                y: ysi,
                mode: "lines",
                type: "scatter",
                name: "oversold (30)",
                line: {
                    color: "red",
                    width: 2
                }
            })

        })
    }
})




//MACD MARK
const macd = document.getElementById('macd');
macd.addEventListener('click', () => {
    Papa.parse("technical_indicators_1.csv", {
        download: true,
        header: true,
        complete: function (results) {
            const xarray = [];
            const MACD = [];
            const MACDsignal = [];
            const MACDhistogramabove = new Array(results.data.length).fill(null);
            const MACDhistogrambelow = new Array(results.data.length).fill(null);

            results.data.forEach((row, index) => {
                xarray.push(row['Date'])
                MACD.push(row['MACD']);
                MACDsignal.push(row['MACD_signal']);
                const histo_value = row['MACD_histogram'];
                if (histo_value > 0) {
                    MACDhistogramabove[index] = (histo_value);
                }
                else {
                    MACDhistogrambelow[index] = (histo_value);
                }
            });
            Plotly.addTraces("myplot", {
                x: xarray,
                y: MACD,
                mode: "lines",
                type: "scatter",
                name: "MACD",
                line: {
                    width: 2,
                    color: "yellow"
                }
            })
            Plotly.addTraces("myplot", {
                x: xarray,
                y: MACDsignal,
                mode: "lines",
                type: "scatter",
                name: "MACDsignals",
                line: {
                    width: 2,
                    color: "blue"
                }
            })
            Plotly.addTraces("myplot", {
                x: xarray,
                y: MACDhistogramabove,
                type: "bar",
                name: "MACDhistogramabove",
                marker: {
                    color: "green"
                }
            })
            Plotly.addTraces("myplot", {
                x: xarray,
                y: MACDhistogrambelow,
                type: "bar",
                name: "MACDhistogrambelow",
                marker: {
                    color: "red"
                }
            })
        }
    })
})