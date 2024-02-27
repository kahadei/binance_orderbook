import {useEffect, useState} from 'react'
import Loader from "./components/UI/Loader.jsx";
import './App.css'
import useFetch from "./hooks/useFetch.jsx";
import Table from 'react-bootstrap/Table';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import CryptoBar from "./components/Charts/CryptoBar.jsx"

function App() {
    const [trades, setTrades] = useState([]);
    const [orders, setOrders] = useState([]);
    const {get} = useFetch('http://127.0.0.1:8000/');


    useEffect(() => {
        let interval = setInterval(() => {
            get('trades')
                .then(data => {
                    for (let trade of data) {
                        trade.event_time = new Date(trade.event_time);
                    }
                    setTrades(data);
                })
                .catch(error => console.error(error))
        }, 2000)
        return () => clearInterval(interval);
    }, [])

    useEffect(() => {
        let interval = setInterval(() => {
            get('orders')
                .then(data => {
                    setOrders(data);
                })
                .catch(error => console.error(error))
        }, 2000)
        return () => clearInterval(interval);
    }, [])

    return (
        <Container>
            <div>
                <Loader/>
            </div>
            <Row>
                <CryptoBar/>
            </Row>
            <Row>
                <Col xs={3} md={3}>
                    <Table responsive>
                        <thead>
                        <tr>
                            <th>side_type</th>
                            <th>price</th>
                            <th>quantity</th>
                        </tr>
                        </thead>
                        <tbody>
                        {orders.filter(order => order.side_type === "asks")
                            .map(order => {
                                return (<tr>
                                    <td>{order.side_type}</td>
                                    <td>{order.price}</td>
                                    <td>{order.quantity}</td>
                                </tr>)

                            })}
                        </tbody>
                    </Table>
                </Col>
                <Col xs={3} md={3}>
                    <Table responsive>
                        <thead>
                        <tr>
                            <th>side_type</th>
                            <th>price</th>
                            <th>quantity</th>
                        </tr>
                        </thead>
                        <tbody>
                        {orders.filter(order => order.side_type === "bids")
                            .map(order => {
                                return (<tr>
                                    <td>{order.side_type}</td>
                                    <td>{order.price}</td>
                                    <td>{order.quantity}</td>
                                </tr>)
                            })}
                        </tbody>
                    </Table>
                </Col>
                <Col xs={6} md={6}>
                    <Table responsive>
                        <thead>
                        <tr>
                            <th>event_type</th>
                            <th>symbol</th>
                            <th>price</th>
                            <th>quantity</th>
                            <th>trade_time</th>
                            <th>market_maker</th>
                        </tr>
                        </thead>
                        <tbody>
                        {trades.map(trade => {
                            return (<tr>
                                <td>{trade.event_type}</td>
                                <td>{trade.symbol}</td>
                                <td>{trade.price}</td>
                                <td>{trade.quantity}</td>
                                <td>{trade.event_time.getHours()}:{trade.event_time.getMinutes()}:{trade.event_time.getSeconds()}</td>
                                <td>{trade.market_maker}</td>
                            </tr>)
                        })}
                        </tbody>
                    </Table>
                </Col>
            </Row>

        </Container>)
}

export default App
