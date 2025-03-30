document.addEventListener('DOMContentLoaded', () => {
    // Navigation Logic
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all nav links and sections
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));

            // Add active class to clicked nav link and corresponding section
            link.classList.add('active');
            const targetSectionId = link.getAttribute('href').substring(1);
            document.getElementById(targetSectionId).classList.add('active');
        });
    });

    // Recommendations Logic
    const recommendBtn = document.getElementById('recommend-btn');
    const genderSelect = document.getElementById('gender-select');
    const occasionSelect = document.getElementById('occasion-select');
    const recommendationResult = document.getElementById('recommendation-result');

    const outfitRecommendations = {
        male: {
            casual: 'casuall.jpeg',
            formal: 'formalll.jpeg',
            sports: 'male3.webp'
        },
        female: {
            casual: 'female1.jpg',
            formal: 'female2.avif',
            sports: 'female3.jpg'
        }
    };

    recommendBtn.addEventListener('click', () => {
        const gender = genderSelect.value;
        const occasion = occasionSelect.value;

        if (gender && occasion) {
            recommendationResult.innerHTML = `
                <h3>${gender.charAt(0).toUpperCase() + gender.slice(1)} ${occasion.charAt(0).toUpperCase() + occasion.slice(1)} Outfit</h3>
                <img src="${outfitRecommendations[gender][occasion]}" alt="Outfit Recommendation">
            `;
        } else {
            recommendationResult.innerHTML = '<p>Please select both gender and occasion.</p>';
        }
    });

    // Occasions Logic
    const occasionItems = document.querySelectorAll('.occasion-item');
    const occasionDetails = document.getElementById('occasion-details');

    occasionItems.forEach(item => {
        item.addEventListener('click', () => {
            const occasion = item.dataset.occasion;
            occasionDetails.innerHTML = `
                <h3>${occasion.charAt(0).toUpperCase() + occasion.slice(1)} Outfit</h3>
                <img src="${item.querySelector('img').src}" alt="${occasion} Outfit">
            `;
        });
    });

    // Weather Logic
    const weatherRecommendBtn = document.getElementById('weather-recommend-btn');
    const temperatureInput = document.getElementById('temperature');
    const weatherTypeSelect = document.getElementById('weather-type');
    const weatherResult = document.getElementById('weather-result');

    const weatherOutfits = {
        hot: 'hot.jpg',
        warm: 'warm.jpg',
        cool: 'cool.webp',
        cold: 'cool.webp',
        rainy: 'rainy.jpg'
    };

    weatherRecommendBtn.addEventListener('click', () => {
        const temperature = temperatureInput.value;
        const weatherType = weatherTypeSelect.value;

        let recommendedType = weatherType;
        if (!recommendedType) {
            if (temperature > 30) recommendedType = 'hot';
            else if (temperature > 20) recommendedType = 'warm';
            else if (temperature > 10) recommendedType = 'cool';
            else recommendedType = 'cold';
        }

        if (recommendedType) {
            weatherResult.innerHTML = `
                <h3>${recommendedType.charAt(0).toUpperCase() + recommendedType.slice(1)} Weather Outfit</h3>
                <img src="${weatherOutfits[recommendedType]}" alt="Weather Outfit Recommendation">
            `;
        } else {
            weatherResult.innerHTML = '<p>Please enter temperature or select weather type.</p>';
        }
    });
});

// document.getElementById('recommend-btn').addEventListener('click', () => {
//     const gender = document.getElementById('gender-select').value;
//     const occasion = document.getElementById('occasion-select').value;
//     const output = document.getElementById('recommendation-result');
//     if (gender && occasion) {
//         output.innerHTML = `<p>Recommended ${occasion} outfit for ${gender} selected. Stay stylish!</p>`;
//     } else {
//         output.innerHTML = `<p>Please select both gender and occasion.</p>`;
//     }
// });

// document.querySelectorAll('.occasion-item').forEach(item => {
//     item.addEventListener('click', () => {
//         const occasion = item.getAttribute('data-occasion');
//         document.getElementById('occasion-details').innerHTML = `<p>Here’s a stylish look idea for your ${occasion} occasion. Match with accessories for the perfect vibe!</p>`;
//     });
// });

// document.getElementById('weather-recommend-btn').addEventListener('click', () => {
//     const temp = document.getElementById('temperature').value;
//     const weather = document.getElementById('weather-type').value;
//     const result = document.getElementById('weather-result');

//     if (temp && weather) {
//         result.innerHTML = `<p>It’s ${temp}°C and ${weather}. We recommend layering with breathable and weather-appropriate clothing. Stay comfy and sharp!</p>`;
//     } else {
//         result.innerHTML = `<p>Please enter temperature and select a weather type.</p>`;
//     }
// });

