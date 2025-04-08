// static/js/main.js
$(document).ready(function() {
    // État de l'interface
    let learningMode = false;
    
    // Gestionnaire pour le toggle du mode d'apprentissage
    $('#learningModeToggle').change(function() {
        const isChecked = $(this).is(':checked');
        toggleLearningMode(isChecked);
    });
    
    // Gestionnaire pour le formulaire de message
    $('#messageForm').submit(function(e) {
        e.preventDefault();
        sendMessage();
    });
    
    // Gestionnaire pour le formulaire d'upload
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        uploadFile();
    });
    
    // Charger l'historique des conversations
    loadConversationHistory();
    
    // Fonctions
    function toggleLearningMode(active) {
        $.ajax({
            url: '/api/learning/toggle',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ active: active }),
            success: function(response) {
                learningMode = response.learning_mode;
                updateUI();
            },
            error: function(error) {
                console.error('Erreur lors du changement de mode:', error);
                showStatus('Erreur lors du changement de mode', 'danger');
            }
        });
    }
    
    function updateUI() {
        // Mettre à jour l'affichage du mode
        $('#currentMode').text(learningMode ? 'Apprentissage' : 'Conversation');
        
        // Afficher/masquer la section d'upload de fichiers
        if (learningMode) {
            $('#fileUploadSection').slideDown();
        } else {
            $('#fileUploadSection').slideUp();
        }
        
        // Mettre à jour le switch
        $('#learningModeToggle').prop('checked', learningMode);
        
        // Mettre à jour le message de statut
        showStatus('Mode ' + (learningMode ? 'apprentissage' : 'conversation') + ' activé', 'info');
    }
    
    function sendMessage() {
        const userInput = $('#userInput').val().trim();
        if (!userInput) return;
        
        // Ajouter le message de l'utilisateur à la conversation
        appendMessage(userInput, 'user');
        
        // Vider le champ de saisie
        $('#userInput').val('');
        
        // Montrer un indicateur de chargement
        showStatus('En attente de réponse...', 'info');
        
        // Envoyer le message à l'API
        $.ajax({
            url: '/api/chat',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: userInput }),
            success: function(response) {
                // Ajouter la réponse de l'agent à la conversation
                appendMessage(response.response, 'agent');
                showStatus('Prêt', 'success');
                
                // Mettre à jour l'historique
                loadConversationHistory();
            },
            error: function(error) {
                console.error('Erreur lors de l\'envoi du message:', error);
                showStatus('Erreur lors de l\'envoi du message', 'danger');
            }
        });
    }
    
    function uploadFile() {
        const fileInput = document.getElementById('fileInput');
        if (!fileInput.files || fileInput.files.length === 0) {
            showUploadStatus('Veuillez sélectionner un fichier', 'danger');
            return;
        }
        
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        // Montrer un indicateur de chargement
        showUploadStatus('Téléversement en cours...', 'info');
        
        $.ajax({
            url: '/api/learning/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    showUploadStatus(response.message, 'success');
                    fileInput.value = ''; // Réinitialiser le champ de fichier
                } else {
                    showUploadStatus(response.message, 'danger');
                }
            },
            error: function(error) {
                console.error('Erreur lors du téléversement du fichier:', error);
                showUploadStatus('Erreur lors du téléversement', 'danger');
            }
        });
    }
    
    function appendMessage(content, sender) {
        const messageClass = sender === 'user' ? 'user-message' : 'agent-message';
        const messageHTML = `
            <div class="message ${messageClass}">
                <div class="message-content">
                    ${content}
                </div>
            </div>
        `;
        
        $('#chatMessages').append(messageHTML);
        
        // Faire défiler vers le bas pour voir le nouveau message
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function loadConversationHistory() {
        $.ajax({
            url: '/api/history',
            type: 'GET',
            success: function(response) {
                $('#conversationHistory').empty();
                
                const history = response.history.reverse();
                history.forEach(function(item) {
                    const truncatedUser = truncateText(item.user, 30);
                    const date = new Date(item.timestamp).toLocaleString();
                    
                    const historyItem = `
                        <a href="#" class="list-group-item list-group-item-action" 
                           data-user="${item.user}" data-agent="${item.agent}">
                            <div class="d-flex w-100 justify-content-between">
                                <small>${truncatedUser}</small>
                                <small class="text-muted">${date}</small>
                            </div>
                        </a>
                    `;
                    
                    $('#conversationHistory').append(historyItem);
                });
                
                // Ajouter des gestionnaires d'événements pour les éléments d'historique
                $('.list-group-item').click(function(e) {
                    e.preventDefault();
                    const userMessage = $(this).data('user');
                    const agentMessage = $(this).data('agent');
                    
                    // Afficher l'échange complet dans la fenêtre de conversation
                    $('#chatMessages').empty();
                    appendMessage(userMessage, 'user');
                    appendMessage(agentMessage, 'agent');
                });
            },
            error: function(error) {
                console.error('Erreur lors du chargement de l\'historique:', error);
            }
        });
    }
    
    function showStatus(message, type) {
        const statusMessage = $('#statusMessage');
        statusMessage.text(message);
        
        // Ajouter une classe de couleur basée sur le type
        statusMessage.removeClass('text-success text-danger text-info text-warning');
        switch(type) {
            case 'success': statusMessage.addClass('text-success'); break;
            case 'danger': statusMessage.addClass('text-danger'); break;
            case 'warning': statusMessage.addClass('text-warning'); break;
            case 'info': statusMessage.addClass('text-info'); break;
        }
    }
    
    function showUploadStatus(message, type) {
        const uploadStatus = $('#uploadStatus');
        uploadStatus.text(message);
        
        // Ajouter une classe de couleur basée sur le type
        uploadStatus.removeClass('text-success text-danger text-info text-warning');
        switch(type) {
            case 'success': uploadStatus.addClass('text-success'); break;
            case 'danger': uploadStatus.addClass('text-danger'); break;
            case 'warning': uploadStatus.addClass('text-warning'); break;
            case 'info': uploadStatus.addClass('text-info'); break;
        }
    }
    
    function truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
});