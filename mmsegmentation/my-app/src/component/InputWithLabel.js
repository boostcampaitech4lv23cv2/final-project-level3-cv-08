import React from 'react';
import styled from 'styled-components';
import oc from 'open-color';

const Wrapper = styled.div`
    & + & {
        margin-top: 1rem;
    }
`;

const Label = styled.div`
    font-size: 1rem;
    font-family: 'NanumBarunGothic';
    color: ${oc.gray[6]};
    margin-bottom: 0.25rem;
`;

const Input = styled.input`
    font-family: 'NanumBarunGothic';
    width: 95%;
    border: 1px solid ${oc.gray[3]};
    outline: none;
    border-radius: 10px;
    line-height: 2.5rem;
    font-size: 1.2rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;    
`;

const InputWithLabel = ({label, ...rest}) => (
    <Wrapper>
        <div className="wrapperLabel">
            <Label>{label}</Label>
        </div>
        <div className="wrapperInput">
            <Input {...rest}/>
        </div>
    </Wrapper>
);

export default InputWithLabel;