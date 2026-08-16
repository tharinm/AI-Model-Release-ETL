/**
 * AI Model Tracker & Popularity Predictor Dashboard App
 */

let allModels = [];

document.addEventListener("DOMContentLoaded", () => {
    loadModelData();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById("searchInput").addEventListener("input", filterAndRender);
    document.getElementById("filterTag").addEventListener("change", filterAndRender);
    document.getElementById("filterLibrary").addEventListener("change", filterAndRender);
    document.getElementById("filterLicense").addEventListener("change", filterAndRender);
    document.getElementById("sortSelect").addEventListener("change", filterAndRender);
    document.getElementById("refreshBtn").addEventListener("click", loadModelData);
}

async function loadModelData() {
    const tableBody = document.getElementById("modelTableBody");
    tableBody.innerHTML = `<tr><td colspan="8" class="loading-cell">Fetching latest model metadata...</td></tr>`;

    try {
        // Attempt to fetch generated JSON
        const response = await fetch("../data/processed/models_with_predictions.json");
        if (!response.ok) throw new Error("JSON file not found");
        allModels = await response.json();
    } catch (e) {
        console.warn("Could not load models_with_predictions.json, generating fallback data:", e);
        allModels = generateFallbackModels();
    }

    populateFilterDropdowns();
    updateKPICards();
    renderTopModels(allModels);
    filterAndRender();
}

function updateKPICards() {
    document.getElementById("statTotalModels").textContent = allModels.length.toLocaleString();
    
    const popularCount = allModels.filter(m => (m.popularity_probability || 0) >= 0.5 || m.is_predicted_popular === 1).length;
    document.getElementById("statPopularCount").textContent = popularCount.toLocaleString();

    const totalDownloads = allModels.reduce((acc, m) => acc + (m.downloads || 0), 0);
    document.getElementById("statTotalDownloads").textContent = formatCompactNumber(totalDownloads);

    const totalLikes = allModels.reduce((acc, m) => acc + (m.likes || 0), 0);
    document.getElementById("statTotalLikes").textContent = formatCompactNumber(totalLikes);
}

function renderTopModels(models) {
    const topGrid = document.getElementById("topModelsGrid");
    const title = document.getElementById("topModelsTitle");
    const subtitle = document.getElementById("topModelsSubtitle");
    
    const maxDownloads = models.reduce((max, m) => Math.max(max, m.downloads || 0), 0);
    
    let sorted;
    if (maxDownloads > 0) {
        sorted = [...models].sort((a, b) => (b.downloads || 0) - (a.downloads || 0));
        if (title) title.textContent = "🏆 Most Used Models";
        if (subtitle) subtitle.textContent = "Highest Downloads";
    } else {
        sorted = [...models].sort((a, b) => (b.popularity_probability || 0) - (a.popularity_probability || 0));
        if (title) title.textContent = "🔥 Trending Models";
        if (subtitle) subtitle.textContent = "Highest Popularity Prediction";
    }

    const top5 = sorted.slice(0, 5);

    if (top5.length === 0) {
        topGrid.innerHTML = `<div style="color: var(--color-text-tertiary); font-style: italic;">No top models data available.</div>`;
        return;
    }

    topGrid.innerHTML = top5.map((m, index) => {
        const hfUrl = `https://huggingface.co/${m.model_id}`;
        return `
            <a href="${hfUrl}" target="_blank" class="top-model-card">
                <span class="tmc-rank">#${index + 1}</span>
                <div class="tmc-content">
                    <div class="tmc-title">${escapeHtml(m.model_name || m.model_id.split('/').pop())}</div>
                    <div class="tmc-author">by ${escapeHtml(m.author || 'community')}</div>
                </div>
                <div class="tmc-stats">
                    <div class="tmc-stat" title="Downloads">
                        ⬇️ ${(m.downloads || 0).toLocaleString()}
                    </div>
                    <div class="tmc-stat" title="Likes">
                        ⭐ ${(m.likes || 0).toLocaleString()}
                    </div>
                    <div class="tmc-stat" title="Popularity Prediction" style="margin-left: auto;">
                        🔥 ${Math.round((m.popularity_probability || 0) * 100)}%
                    </div>
                </div>
            </a>
        `;
    }).join("");
}

function populateFilterDropdowns() {
    const tags = new Set();
    const libraries = new Set();
    const licenses = new Set();

    allModels.forEach(m => {
        if (m.pipeline_tag && m.pipeline_tag !== "unspecified") tags.add(m.pipeline_tag);
        if (m.library && m.library !== "other") libraries.add(m.library);
        if (m.license && m.license !== "unknown") licenses.add(m.license);
    });

    populateSelect("filterTag", Array.from(tags).sort(), "All Categories");
    populateSelect("filterLibrary", Array.from(libraries).sort(), "All Libraries");
    populateSelect("filterLicense", Array.from(licenses).sort(), "All Licenses");
}

function populateSelect(elementId, options, defaultLabel) {
    const select = document.getElementById(elementId);
    const currentVal = select.value;
    select.innerHTML = `<option value="ALL">${defaultLabel}</option>`;
    options.forEach(opt => {
        const optionEl = document.createElement("option");
        optionEl.value = opt;
        optionEl.textContent = opt;
        select.appendChild(optionEl);
    });
    if (options.includes(currentVal)) {
        select.value = currentVal;
    }
}

function filterAndRender() {
    const query = document.getElementById("searchInput").value.toLowerCase().trim();
    const selectedTag = document.getElementById("filterTag").value;
    const selectedLib = document.getElementById("filterLibrary").value;
    const selectedLic = document.getElementById("filterLicense").value;
    const sortVal = document.getElementById("sortSelect").value;

    let filtered = allModels.filter(m => {
        const matchesQuery = !query || 
            m.model_id.toLowerCase().includes(query) || 
            (m.author && m.author.toLowerCase().includes(query)) ||
            (m.tags && m.tags.toLowerCase().includes(query));

        const matchesTag = selectedTag === "ALL" || m.pipeline_tag === selectedTag;
        const matchesLib = selectedLib === "ALL" || m.library === selectedLib;
        const matchesLic = selectedLic === "ALL" || m.license === selectedLic;

        return matchesQuery && matchesTag && matchesLib && matchesLic;
    });

    // Sorting
    filtered.sort((a, b) => {
        if (sortVal === "pred_desc") return (b.popularity_probability || 0) - (a.popularity_probability || 0);
        if (sortVal === "dl_desc") return (b.downloads || 0) - (a.downloads || 0);
        if (sortVal === "likes_desc") return (b.likes || 0) - (a.likes || 0);
        if (sortVal === "newest") return new Date(b.created_at || 0) - new Date(a.created_at || 0);
        return 0;
    });

    renderTable(filtered);
}

function renderTable(models) {
    const tableBody = document.getElementById("modelTableBody");
    
    if (models.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="8" class="loading-cell">No models matching criteria found.</td></tr>`;
        return;
    }

    tableBody.innerHTML = models.map(m => {
        const prob = Math.round((m.popularity_probability || 0) * 100);
        let fillClass = "fill-low";
        if (prob >= 70) fillClass = "fill-high";
        else if (prob >= 40) fillClass = "fill-med";

        const hfUrl = `https://huggingface.co/${m.model_id}`;

        return `
            <tr>
                <td>
                    <div class="model-id-cell">
                        <a href="${hfUrl}" target="_blank" class="model-title">${escapeHtml(m.model_id)}</a>
                        <span class="author-tag">by ${escapeHtml(m.author || 'community')}</span>
                    </div>
                </td>
                <td><span class="chip chip-purple">${escapeHtml(m.pipeline_tag || 'unspecified')}</span></td>
                <td><span class="chip chip-cyan">${escapeHtml(m.library || 'other')}</span></td>
                <td><span class="chip">${escapeHtml(m.license || 'unknown')}</span></td>
                <td><strong>${(m.downloads || 0).toLocaleString()}</strong></td>
                <td><strong>${(m.likes || 0).toLocaleString()}</strong></td>
                <td>
                    <div class="prob-container">
                        <div class="prob-bar-bg">
                            <div class="prob-bar-fill ${fillClass}" style="width: ${prob}%;"></div>
                        </div>
                        <span class="prob-text">${prob}%</span>
                    </div>
                </td>
                <td>
                    <a href="${hfUrl}" target="_blank" class="btn btn-primary" style="padding: 0.3rem 0.7rem; font-size: 0.78rem;">
                        View HF
                    </a>
                </td>
            </tr>
        `;
    }).join("");
}

function formatCompactNumber(num) {
    if (num >= 1e6) return (num / 1e6).toFixed(1) + "M";
    if (num >= 1e3) return (num / 1e3).toFixed(1) + "K";
    return num.toString();
}

function escapeHtml(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function generateFallbackModels() {
    const pipelines = ["text-generation", "text-to-image", "image-classification", "automatic-speech-recognition"];
    const libs = ["transformers", "diffusers", "timm", "vllm"];
    const authors = ["meta-llama", "mistralai", "google", "deepseek-ai", "microsoft"];
    const licenses = ["apache-2.0", "mit", "llama3"];

    const list = [];
    for (let i = 1; i <= 20; i++) {
        const author = authors[i % authors.length];
        const downloads = Math.floor(Math.random() * 200000) + 500;
        const likes = Math.floor(downloads * (Math.random() * 0.05 + 0.01));
        const prob = Math.round((Math.random() * 0.6 + 0.35) * 100) / 100;
        
        list.push({
            model_id: `${author}/model-release-${i}`,
            author: author,
            pipeline_tag: pipelines[i % pipelines.length],
            library: libs[i % libs.length],
            license: licenses[i % licenses.length],
            downloads: downloads,
            likes: likes,
            created_at: new Date(Date.now() - i * 86400000).toISOString(),
            popularity_probability: prob,
            is_predicted_popular: prob >= 0.5 ? 1 : 0
        });
    }
    return list;
}
