import React from 'react';
import { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';

function InferenceResult(){
    const onFeedbackClick = () => {
        console.log("click!!!!");
        alert("전송되었습니다!");
    }

    const TextH4 = styled.h4`
        font-family: 'NanumBarunGothic';
        width: 95%;
        outline: none;
        line-height: 2.5rem;
        font-size: 1.2rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;    
    `;


    return(
        <div align="center">
            <TextH4>결과 확인</TextH4>

            <h2>결과 어케 보여주지</h2>
            
            <div align="center">
                <button className="submitButton"
                    onClick={onFeedbackClick}
                    style={{backgroundColor: "#0095f6",
                        borderRadius: 10,
                        padding: "10px 20px",
                        border: 0,
                        color: "white",
                        fontSize: "1.2rem",
                        fontFamily: "NanumBarunGothic",
                        display: "inline-block",}}>
                    피드백 전송
                </button>
            </div>
        </div>  
    );
}

export default InferenceResult;