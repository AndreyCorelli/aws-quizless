function getRadioGroupValue(selector) {
    const radios = document.querySelectorAll(selector);
    let selectedValue;
    radios.forEach(radio => {
        if (radio.checked) selectedValue = radio.value;
    });
    return selectedValue;
}

function getSelectedCheckboxes(container) {
    const checkboxes = container.querySelectorAll("input[type='checkbox']");
    const selectedIndexes = [];
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            selectedIndexes.push(i);
        }
    }
    return selectedIndexes;
}

function encodeHTML(text) {
    const dummyElement = document.createElement('div');
    dummyElement.innerText = text;
    return dummyElement.innerHTML;
}

function deleteAllChildren(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function createRadioGroup(nameValue, nameGetter,
    valueGetter, parentDiv, labelClass, inputName) {
    labelClass = labelClass || 'topics-radio-group';

    const radioGroup = document.createElement('div');
    nameValue.forEach(topic => {
        const label = document.createElement('label');
        label.classList.add(labelClass);
        const radio = document.createElement('input');

        radio.type = 'radio';
        radio.name = inputName;
        radio.value = valueGetter(topic);

        label.textContent = nameGetter(topic);
        label.appendChild(radio);

        radioGroup.appendChild(label);
    });
    parentDiv.appendChild(radioGroup);
}

function createCheckboxes(nameValue, nameGetter, valueGetter, parentDiv, labelClass) {
    nameValue.forEach(topic => {
        const name = nameGetter(topic);
        const value = valueGetter(topic);
        const label = document.createElement("label");
        label.classList.add(labelClass);
        label.textContent = name;

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = value;

        label.appendChild(checkbox);
        parentDiv.appendChild(label);
    });
}
