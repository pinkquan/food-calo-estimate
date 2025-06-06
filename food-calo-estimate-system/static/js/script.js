// document.addEventListener('DOMContentLoaded', function() {
//     // DOM Elements
//     const dropZone = document.getElementById('dropZone');
//     const fileInput = document.getElementById('fileInput');
//     const analyzeBtn = document.getElementById('analyzeBtn');
//     const imagePreview = document.getElementById('imagePreview');
//     const previewSection = document.getElementById('previewSection');
//     const resultsSection = document.getElementById('resultsSection');
//     const loadingSpinner = document.getElementById('loadingSpinner');
//     const resultsContainer = document.getElementById('resultsContainer');
//     const detectedObjects = document.getElementById('detectedObjects');
//     const resultsTableBody = document.getElementById('resultsTableBody');
    
//     // Khởi tạo biến lưu trữ file đã chọn
//     let selectedFile = null;
    
//     // Color mapping for object classes
//     const colorMap = {
//         'coin': '#FFD700',      // Gold
//         'apple': '#FF5252',     // Red
//         'banana': '#FFEB3B',    // Yellow
//         'bread': '#A1887F',     // Brown
//         'bun': '#E6C3A5',       // Light brown
//         'doughnut': '#FF9E80',  // Light orange
//         'egg': '#FFFDE7',       // Off-white
//         'fired_dough_twist': '#FFCC80', // Light orange
//         'grape': '#9C27B0',     // Purple
//         'lemon': '#FFFF00',     // Yellow
//         'litchi': '#F48FB1',    // Pink
//         'mango': '#FFAB40',     // Orange
//         'mooncake': '#8D6E63',  // Brown
//         'orange': '#FF9800',    // Orange
//         'pear': '#AED581',      // Light green
//         'peach': '#FFAB91',     // Peach
//         'plum': '#673AB7',      // Dark purple
//         'qiwi': '#8BC34A',      // Green
//         'sachima': '#E6AA68',   // Tan
//         'tomato': '#FF5252'     // Red
//     };
    
//     dropZone.addEventListener('dragover', (event) => {
//         event.preventDefault();
//         dropZone.classList.add('drag-over');
//     });
    
//     dropZone.addEventListener('dragleave', () => {
//         dropZone.classList.remove('drag-over');
//     });
    
//     dropZone.addEventListener('drop', (event) => {
//         event.preventDefault();
//         dropZone.classList.remove('drag-over');
//         selectedFile = event.dataTransfer.files[0];
//         displayImagePreview();
//     });
//     fileInput.addEventListener('change', () => {
//         selectedFile = fileInput.files[0];
//         displayImagePreview();
//     });

//     function displayImagePreview() {
//         if (selectedFile) {
//             const imageUrl = URL.createObjectURL(selectedFile);
//             imagePreview.src = imageUrl;
//             previewSection.style.display = 'block';
//         }
//     }
    
//     analyzeBtn.addEventListener('click', () => {
//         if (selectedFile) {
//             analyzeImage();
//         }
//     });
    
//     async function analyzeImage() {
//         try {
//             loadingSpinner.style.display = 'block';
//             resultsSection.style.display = 'none';
    
//             const formData = new FormData();
//             formData.append('image', selectedFile);
    
//             const response = await fetch('/analyze', {
//                 method: 'POST',
//                 body: formData
//             });
    
//             const data = await response.json();
    
//             displayResults(data);
//         } catch (error) {
//             console.error('Error analyzing image:', error);
//         } finally {
//             loadingSpinner.style.display = 'none';
//         }
//     }
    
//     function displayResults(data) {
//         resultsSection.style.display = 'block';
    
//         // Clear previous results
//         resultsTableBody.innerHTML = '';
    
//         // Populate results table
//         data.forEach((item) => {
//             const row = document.createElement('tr');
    
//             const objectNameCell = document.createElement('td');
//             objectNameCell.textContent = item.name;
//             objectNameCell.style.color = colorMap[item.name.toLowerCase()];
    
//             const weightCell = document.createElement('td');
//             weightCell.textContent = item.weight.toFixed(2) + ' g';
    
//             const caloriesCell = document.createElement('td');
//             caloriesCell.textContent = item.calories.toFixed(2) + ' kcal';
    
//             row.appendChild(objectNameCell);
//             row.appendChild(weightCell);
//             row.appendChild(caloriesCell);
//             resultsTableBody.appendChild(row);
//         });
    
//         detectedObjects.textContent = `Detected ${data.length} objects`;
//         resultsContainer.style.display = 'block';
//     }
    
//     const browseBtn = document.querySelector('.browse-btn');
//     browseBtn.addEventListener('click', () => {
//         fileInput.click();
//     });

// })
// DOM elements
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('preview-container');
const previewImage = document.getElementById('preview-image');
const analyzeBtn = document.getElementById('analyze-btn');
const deleteBtn = document.getElementById('delete-btn');
const loadingElement = document.getElementById('loading');
const resultsContainer = document.getElementById('results-container');
const resultsBody = document.getElementById('results-body');
const totalCalories = document.getElementById('total-calories');
const errorMessage = document.getElementById('error-message');

let currentFile = null;

function initDragAndDrop() {
    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', handleFileSelect);

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener('drop', handleDrop, false);
}
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight() {
    dropArea.classList.add('highlight');
}

function unhighlight() {
    dropArea.classList.remove('highlight');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length) {
        handleFiles(files);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length) {
        handleFiles(files);
    }
}

function handleFiles(files) {
    if (files[0].type.startsWith('image/')) {
        currentFile = files[0];
        displayPreview(files[0]);
    } else {
        showError("Please select an image file (JPEG, PNG, etc.)");
    }
}

function displayPreview(file) {
    previewContainer.style.display = 'block';
    dropArea.style.display = 'none';
    
    const fileURL = URL.createObjectURL(file);
    previewImage.src = fileURL;
    
    resultsContainer.style.display = 'none';
    errorMessage.style.display = 'none';
}

function resetUpload() {
    fileInput.value = '';
    currentFile = null;
    
    dropArea.style.display = 'block';
    previewContainer.style.display = 'none';
    
    resultsContainer.style.display = 'none';
    errorMessage.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    loadingElement.style.display = 'none';
}

function analyzeImage() {
    if (!currentFile) {
        showError("Please select an image first.");
        return;
    }
    
    loadingElement.style.display = 'flex';
    resultsContainer.style.display = 'none';
    errorMessage.style.display = 'none';
    
    const formData = new FormData();
    formData.append('file', currentFile);
    
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }
        
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error(`Expected JSON response but got ${contentType}`);
        }
        
        return response.json();
    })
    .then(data => {
        loadingElement.style.display = 'none';
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        displayResults(data);
    })
    .catch(error => {
        loadingElement.style.display = 'none';
        console.error("Error details:", error);
        showError("Error analyzing image: " + error.message);
    });
}

function displayResults(data) {
    resultsBody.innerHTML = '';
    
    if (!data.results || data.results.length === 0) {
        showError("No food items detected in the image.");
        return;
    }
    
    let caloriesSum = 0;
    
    data.results.forEach(item => {
        const row = document.createElement('tr');
        const confidencePercent = (item.confidence * 100).toFixed(0) + '%';
        
        row.innerHTML = `
            <td>${capitalizeFirstLetter(item.name)}</td>
            <td>${confidencePercent}</td>
            <td>${item.volume_cm3} cm³</td>
            <td>${item.weight_g} g</td>
            <td>${item.calories} kcal</td>
        `;
        
        resultsBody.appendChild(row);
        caloriesSum += item.calories;
    });
    
    totalCalories.textContent = caloriesSum.toFixed(2) + ' kcal';
    
    resultsContainer.style.display = 'block';
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

document.addEventListener('DOMContentLoaded', () => {
    initDragAndDrop();
    analyzeBtn.addEventListener('click', analyzeImage);
    deleteBtn.addEventListener('click', resetUpload);
});