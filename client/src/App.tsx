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

interface GraphInfo {
    data: {
        labels: number[],
        datasets: [
            {
                label: string,
                data: number[],
                fill: boolean,
                borderColor: string,
                tension: number
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

    const days = [...Array(31).keys()]
    days.shift()
    
    const makeDiagram = (label: string, data: number[]): GraphInfo => {
        return {
            data: {
                labels: days,
                datasets: [
                    {
                        label: label,
                        data: data,
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
    }

    useEffect(() => {
        getData();
    }, []);

    console.dir(details)

    

    const diagrams = [
        makeDiagram('Amount of working stoves', details.map((detail: Details) => detail.amount_of_stoves)),
        makeDiagram('Amount of working stoves', details.map((detail: Details) => detail.average_number_of_hours)),
        makeDiagram('Amount of working stoves', details.map((detail: Details) => detail.number)),
        makeDiagram('Amount of working stoves', details.map((detail: Details) => detail.amount_of_stoves)),
    
    ]

    

    const missionInfo: string = `Использование печек существенно снижает потребление древесины, а следовательно и выброс CO2 в атмосферу.
    180.works хочет получить дополнительное финансирование за счет участия в программе Carbon Credits - ценные бумаги, которые выдаются за снижение выбросов CO2.
    Но для этого необходимо знать реальное использование печек.
    Сейчас компания исследует возможность встраивания в печки термодатчиков передающих данные по LoRaWAN протоколу.`



    const mainSiteReference: ReactElement = <a href="https://180.works/#/carbon-offset">180.works</a>

    return (
        <div>
            <div className="header">
                <div className="header__background-image"></div>
                <div className="header__content">
                    <h1>Let's save Africa</h1>
                    <p>Некоммерческая организация {mainSiteReference} занимается восстановлением лесов в Африке. Частью этой программы является установка печек для приготовления пищи.

                    </p>
                    <p>{missionInfo}</p>
                </div>
            </div>

            <div className='diagrams-container'>
                {diagrams.map(({ data, options }, index) => <div className="diagrams-container__chart" key={index}>
                    <Graph data={data} options={options} />
                </div>)}
            </div>

            <div className="region-table">
                <Table />
            </div>


            <div className="about">
                {details.map(({
                    number,
                    date,
                    amount_of_stoves,
                    average_number_of_hours }, index) => <div key={index} className='about__paragraph'>
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