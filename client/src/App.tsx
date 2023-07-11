import React, { FC, ReactElement, useState, useEffect } from 'react';
import Graph from './components/Graph';
import './App.css'
import Table from './components/Table';
import axios from 'axios'

interface Details {
    number: number,
    date: string,
    amount_of_stoves: number,
    average_number_of_hours: number
}

const App: FC = () => {

    const [details, setDetails] = useState<Array<Details>>([{
        number: 1,
        date: 'string',
        amount_of_stoves: 1,
        average_number_of_hours: 1
    }])


    const getData = async () => {
        const { data } = await axios.get('http://127.0.0.1:8000/?format=json');
        setDetails(data);
    };

    useEffect(() => {
        getData();
    }, []);

    console.dir(details)

    const days = [...Array(31).keys()]
    days.shift()

    const diagrams = [{
        data: {
            labels: days,
            datasets: [
                {
                    label: 'Amount of working stoves',
                    data: details.map((detail: Details) => detail.amount_of_stoves),
                    fill: false,
                    borderColor: 'rgb(89, 84, 86)',
                    tension: 0.5
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    },
    {
        data: {
            labels: days,
            datasets: [
                {
                    label: 'My Second Dataset',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    fill: false,
                    borderColor: 'rgb(89, 84, 86)',
                    tension: 0.1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    },
    {
        data: {
            labels: days,
            datasets: [
                {
                    label: 'My Third Dataset',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    fill: false,
                    borderColor: 'rgb(89, 84, 86)',
                    tension: 0.1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    },
    {
        data: {
            labels: days,
            datasets: [
                {
                    label: 'My Fourth Dataset',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    fill: false,
                    borderColor: 'rgb(89, 84, 86)',
                    tension: 0.1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
    ]

    const missionInfo: string = `Использование печек существенно снижает потребление древесины, а следовательно и выброс CO2 в атмосферу.
    180.works хочет получить дополнительное финансирование за счет участия в программе Carbon Credits - ценные бумаги, которые выдаются за снижение выбросов CO2.
    Но для этого необходимо знать реальное использование печек.
    Сейчас компания исследует возможность встраивания в печки термодатчиков передающих данные по LoRaWAN протоколу.`

    const mainSiteReference: ReactElement = <a href="https://180.works/#/carbon-offset">180.works</a>

    return (
        <div>
            <div className="App-header">
                <div className="background"></div>
                <div className="content">
                    <h1>Let's save Africa</h1>
                    <p>Некоммерческая организация {mainSiteReference} занимается восстановлением лесов в Африке. Частью этой программы является установка печек для приготовления пищи.

                    </p>
                    <p>{missionInfo}</p>
                </div>
            </div>

            <div className='diagrams'>
                {diagrams.map(({ data, options }, index) => <div className="diagram" key={index}>
                    <Graph data={data} options={options} />
                </div>)}
            </div>

            <div className="table-container">
                <Table />
            </div>


            <div className="short-numbers">
                {details.map(({
                    number,
                    date,
                    amount_of_stoves,
                    average_number_of_hours }, index) => <div key={index} className='company-fact'>
                        <p>Amount of stoves:</p>
                        <p> {amount_of_stoves}</p>
                        <p>Average number of hours:</p>
                        <p>{average_number_of_hours}</p>
                    </div>)}
            </div>
            <footer>
                <p>Copyright © 2023 Byelex. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default App;