import React, {PureComponent, useEffect, useState} from 'react';
import {
    BarChart,
    LineChart,
    Bar,
    Cell,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ReferenceLine,
    ResponsiveContainer,
    Line
} from 'recharts';
import useFetch from "../../hooks/useFetch.jsx";
import {Figure} from "react-bootstrap";
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';


export default function CryptoBar() {
    const [minutesFilter, setMinutesFilter] = useState('30');
    const [trade_by_min, setTradesByMin] = useState([]);
    const [trades_sum, setTradeSum] = useState([]);
    const [averPrice, setAverPrice] = useState(0);
    const {get} = useFetch('https://manhattan.foundation/');

    useEffect(() => {
        let interval = setInterval(() => {
            let url = `trades-by-min?min_filter=${minutesFilter}`
            get(url)
                .then(data => {
                    let result = [];
                    let aver_price_sum = 0;
                    let trades_aggr = {
                        name: "Trades sum",
                        sells_sum: 0,
                        buys_sum: 0
                    };
                    let trades_result = [];
                    for (let trade of data) {
                        let sell_quantity = trade.sell_quantity;
                        let buy_quantity = trade.buy_quantity;
                        let trade_time = new Date(trade.trade_time);
                        aver_price_sum = aver_price_sum + trade.sell_average_price;
                        let updated_trade = {
                            ...trade, ...{
                                sell_quantity: -1 * sell_quantity,
                                trade_time: trade_time.getMinutes()
                            }
                        };
                        trades_aggr.sells_sum = trades_aggr.sells_sum + sell_quantity
                        trades_aggr.buys_sum = trades_aggr.buys_sum + buy_quantity
                        result.push(updated_trade)
                    }
                    let aver_price = aver_price_sum / data.length;
                    trades_result.push(trades_aggr)
                    setAverPrice(aver_price);
                    setTradesByMin(result.reverse());
                    setTradeSum(trades_result);
                })
                .catch(error => console.error(error))
        }, 1000)
        return () => clearInterval(interval);
    }, [get, minutesFilter])

    return (
        <Figure>

            <Container>
                <Row className="justify-content-md-center">
                    <Col></Col>
                    <Col xs={2} md={2} lg={2}>
                        <Form.Select aria-label="Default select example"
                            onChange={event => setMinutesFilter(event.target.value)}
                            defaultValue={minutesFilter}
                        >
                            <option value="30">30</option>
                            <option value="60">60</option>
                            <option value="120">120</option>
                            <option value="240">240</option>
                        </Form.Select></Col>
                    <Col></Col>
                </Row>
            </Container>
            <br/>
            <BarChart
                width={1200}
                height={400}
                data={trade_by_min}
                stackOffset="sign"
                margin={{
                    top: 5,
                    right: 10,
                    left: 10,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="trade_time"/>
                <YAxis/>
                <Tooltip/>
                <Legend/>
                <ReferenceLine y={0} stroke="#000"/>
                <Bar dataKey="buy_quantity" fill="#8884d8" name="Buy by min" stackId="stack"/>
                <Bar dataKey="sell_quantity" fill="#82ca9d" name="Sell by min" stackId="stack"/>
            </BarChart>
            <LineChart width={1200} height={400} data={trade_by_min}>
                <XAxis dataKey="trade_time"/>
                <YAxis domain={[averPrice, averPrice]}/>
                <Tooltip/>
                <Legend/>
                <CartesianGrid stroke="#eee" strokeDasharray="3 3"/>
                <Line type="monotone" dataKey="sell_average_price" name="Sell average" stroke="#8884d8"/>
            </LineChart>
            <BarChart
                width={1200}
                height={400}
                data={trades_sum}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="name"/>
                <YAxis/>
                <Tooltip/>
                <Legend/>
                <Bar dataKey="buys_sum" name="Buy sum" fill="#8884d8"/>
                <Bar dataKey="sells_sum" name="Sell sum" fill="#82ca9d"/>
            </BarChart>
        </Figure>
    )
        ;

}