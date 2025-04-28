// static/js/main.js

/**
 * Script principal para o Sistema de Autoavaliação de Segurança Cibernética
 */

document.addEventListener('DOMContentLoaded', function() {
  // Inicializar tooltips do Bootstrap
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function(tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Inicializar popovers do Bootstrap
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function(popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl, {
          trigger: 'focus'
      });
  });

  // Configurar animações fade-in
  document.querySelectorAll('.fade-in').forEach((element, index) => {
      setTimeout(() => {
          element.style.opacity = '1';
          element.style.transform = 'translateY(0)';
      }, 100 * index);
  });

  // Manipulador para atualização de status de recomendação
  setupRecommendationStatusUpdates();

  // Configurar funções específicas de páginas
  setupAssessmentForm();
  setupCompareAssessments();
});

/**
* Configura o manipulador de eventos para atualização de status de recomendações
*/
function setupRecommendationStatusUpdates() {
  const statusUpdaters = document.querySelectorAll('.recommendation-status-update');
  
  statusUpdaters.forEach(element => {
      element.addEventListener('change', function() {
          const recommendationId = this.dataset.recommendationId;
          const assessmentId = this.dataset.assessmentId;
          const status = this.value;
          
          updateRecommendationStatus(assessmentId, recommendationId, status);
      });
  });
}

/**
* Envia requisição para atualizar status de uma recomendação
*/
function updateRecommendationStatus(assessmentId, recommendationId, status) {
  fetch(`/assessment/assessments/${assessmentId}/recommendations/${recommendationId}/status`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: status })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Atualizar UI com novo status
          const badge = document.querySelector(`#recommendation-${recommendationId}-badge`);
          
          // Remover classes de status anteriores
          badge.classList.remove('pending', 'in-progress', 'implemented');
          
          // Adicionar nova classe de status
          badge.classList.add(status);
          
          // Atualizar texto
          let statusText = '';
          if (status === 'pending') statusText = 'Pendente';
          else if (status === 'in-progress') statusText = 'Em Progresso';
          else if (status === 'implemented') statusText = 'Implementado';
          
          badge.textContent = statusText;
          
          // Mostrar notificação de sucesso
          showNotification('Status atualizado com sucesso!', 'success');
      } else {
          // Mostrar erro
          showNotification('Erro ao atualizar status. Tente novamente.', 'danger');
      }
  })
  .catch(error => {
      console.error('Erro:', error);
      showNotification('Erro de conexão. Verifique sua internet.', 'danger');
  });
}

/**
* Mostra uma notificação temporária na tela
*/
function showNotification(message, type = 'info') {
  // Criar elemento de notificação
  const notification = document.createElement('div');
  notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
  notification.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  
  // Adicionar ao corpo do documento
  document.body.appendChild(notification);
  
  // Aplicar estilo
  Object.assign(notification.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      zIndex: '9999',
      minWidth: '300px',
      boxShadow: '0 3px 10px rgba(0,0,0,0.15)',
      borderRadius: '8px'
  });
  
  // Remover após 3 segundos
  setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
          notification.remove();
      }, 300);
  }, 3000);
}

/**
* Configura os manipuladores do formulário de avaliação
*/
function setupAssessmentForm() {
  const assessmentForm = document.getElementById('assessment-form');
  
  if (!assessmentForm) return;
  
  // Validar envio do formulário
  assessmentForm.addEventListener('submit', function(event) {
      if (this.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
          
          // Destacar campos obrigatórios não preenchidos
          this.querySelectorAll('[required]').forEach(input => {
              if (!input.value) {
                  input.classList.add('is-invalid');
              }
          });
          
          // Verificar se todas as questões foram respondidas
          if (document.querySelector('button[name="finish"]') === event.submitter) {
              const unansweredQuestions = document.querySelectorAll('.question-card:not(.answered)');
              
              if (unansweredQuestions.length > 0) {
                  event.preventDefault();
                  
                  // Destacar questões não respondidas
                  unansweredQuestions.forEach(card => {
                      card.classList.add('border-danger');
                      // Adicionar mensagem de alerta
                      const alertText = document.createElement('div');
                      alertText.className = 'text-danger mt-2';
                      alertText.innerHTML = '<i class="fas fa-exclamation-circle"></i> Esta questão precisa ser respondida';
                      card.querySelector('.card-body').appendChild(alertText);
                  });
                  
                  // Rolar até a primeira questão não respondida
                  unansweredQuestions[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                  
                  // Mostrar alerta
                  showNotification('Por favor, responda todas as questões antes de concluir a avaliação.', 'warning');
              }
          }
      }
      
      this.classList.add('was-validated');
  });
  
  // Marcar questões como respondidas quando uma opção é selecionada
  assessmentForm.querySelectorAll('input[type="radio"]').forEach(radio => {
      radio.addEventListener('change', function() {
          const questionCard = this.closest('.question-card');
          
          if (questionCard) {
              // Marcar como respondida
              questionCard.classList.add('answered');
              questionCard.classList.remove('border-danger');
              
              // Remover mensagem de alerta se existir
              const alertText = questionCard.querySelector('.text-danger');
              if (alertText) alertText.remove();
          }
      });
  });
  
  // Atualizar a barra de progresso
  updateAnsweredProgress();
  
  // Adicionar evento para quando uma questão é respondida
  assessmentForm.addEventListener('change', function(event) {
      if (event.target.type === 'radio') {
          updateAnsweredProgress();
      }
  });
}

/**
 * Atualiza a barra de progresso do questionário
 */
function updateAnsweredProgress() {
  const progressBar = document.getElementById('assessment-progress');
  
  if (!progressBar) return;
  
  const totalQuestions = document.querySelectorAll('.question-card').length;
  const answeredQuestions = document.querySelectorAll('.question-card.answered').length;
  
  // Calcular porcentagem
  const percentage = totalQuestions > 0 ? (answeredQuestions / totalQuestions) * 100 : 0;
  
  // Atualizar barra de progresso
  progressBar.style.width = `${percentage}%`;
  progressBar.setAttribute('aria-valuenow', percentage);
  
  // Atualizar texto de progresso
  const progressText = document.getElementById('progress-text');
  if (progressText) {
      progressText.textContent = `${answeredQuestions}/${totalQuestions} questões respondidas (${Math.round(percentage)}%)`;
  }
}

/**
 * Configura a funcionalidade de comparação de avaliações
 */
function setupCompareAssessments() {
  const compareForm = document.getElementById('compare-form');
  
  if (!compareForm) return;
  
  compareForm.addEventListener('submit', function(event) {
      event.preventDefault();
      
      // Obter IDs das avaliações selecionadas
      const assessmentIds = [];
      this.querySelectorAll('input[name="assessment_ids"]:checked').forEach(checkbox => {
          assessmentIds.push(checkbox.value);
      });
      
      // Validar seleção
      if (assessmentIds.length < 1 || assessmentIds.length > 3) {
          showNotification('Selecione de 1 a 3 avaliações para comparar.', 'warning');
          return;
      }
      
      // Solicitar dados para comparação
      fetch('/dashboard/api/compare', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ assessment_ids: assessmentIds })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              renderComparisonChart(data);
          } else {
              showNotification(data.message || 'Erro ao comparar avaliações.', 'danger');
          }
      })
      .catch(error => {
          console.error('Erro:', error);
          showNotification('Erro ao processar a solicitação.', 'danger');
      });
  });
}

/**
 * Renderiza o gráfico de comparação de avaliações
 */
function renderComparisonChart(data) {
  const chartContainer = document.getElementById('comparison-chart');
  
  if (!chartContainer) return;
  
  // Criar canvas para o gráfico
  chartContainer.innerHTML = '<canvas id="comparisonCanvas"></canvas>';
  
  // Preparar dados para o gráfico
  const datasets = [];
  const colors = ['#3a6df0', '#28a745', '#ffc107'];
  
  data.assessments.forEach((assessment, index) => {
      datasets.push({
          label: `${assessment.title} (${assessment.created_at})`,
          data: [
              assessment.scores.network,
              assessment.scores.credentials,
              assessment.scores.malware,
              assessment.scores.backup,
              assessment.scores.compliance,
              assessment.scores.total
          ],
          backgroundColor: `${colors[index]}33`,
          borderColor: colors[index],
          borderWidth: 2,
          pointBackgroundColor: colors[index],
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: colors[index]
      });
  });
  
  // Criar gráfico
  const ctx = document.getElementById('comparisonCanvas').getContext('2d');
  new Chart(ctx, {
      type: 'radar',
      data: {
          labels: data.categories,
          datasets: datasets
      },
      options: {
          responsive: true,
          scales: {
              r: {
                  angleLines: {
                      display: true
                  },
                  suggestedMin: 0,
                  suggestedMax: 100
              }
          }
      }
  });
  
  // Exibir legendas adicionais e info de comparação
  const comparisonResultsDiv = document.getElementById('comparison-results');
  if (comparisonResultsDiv) {
      let resultsHTML = '<div class="row mt-4">';
      
      // Calcular diferenças entre avaliações
      if (data.assessments.length > 1) {
          const newest = data.assessments[0];
          const oldest = data.assessments[data.assessments.length - 1];
          
          // Calcular diferença na pontuação total
          const totalDiff = newest.scores.total - oldest.scores.total;
          const totalDiffClass = totalDiff >= 0 ? 'text-success' : 'text-danger';
          const totalDiffIcon = totalDiff >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
          
          resultsHTML += `
          <div class="col-md-6 mb-4">
              <div class="card shadow-sm h-100">
                  <div class="card-body">
                      <h5 class="card-title">Evolução da Pontuação Total</h5>
                      <div class="d-flex align-items-center">
                          <h3 class="${totalDiffClass} me-2">${Math.abs(totalDiff).toFixed(1)}%</h3>
                          <i class="fas ${totalDiffIcon} ${totalDiffClass}"></i>
                          <span class="ms-2">desde ${oldest.created_at}</span>
                      </div>
                      <p class="text-muted mt-2">
                          ${totalDiff >= 0 ? 
                              'Houve um progresso positivo na segurança cibernética.' : 
                              'A pontuação diminuiu desde a avaliação anterior.'}
                      </p>
                  </div>
              </div>
          </div>`;
          
          // Identificar categoria com maior avanço
          const categories = ['network', 'credentials', 'malware', 'backup', 'compliance'];
          const categoryNames = {
              'network': 'Segurança de Rede',
              'credentials': 'Controle de Acesso',
              'malware': 'Proteção contra Malware',
              'backup': 'Backup e Recuperação',
              'compliance': 'Conformidade'
          };
          
          let maxImprovement = -100;
          let mostImprovedCategory = '';
          
          categories.forEach(category => {
              const diff = newest.scores[category] - oldest.scores[category];
              if (diff > maxImprovement) {
                  maxImprovement = diff;
                  mostImprovedCategory = category;
              }
          });
          
          if (mostImprovedCategory && maxImprovement > 0) {
              resultsHTML += `
              <div class="col-md-6 mb-4">
                  <div class="card shadow-sm h-100">
                      <div class="card-body">
                          <h5 class="card-title">Maior Progresso</h5>
                          <div class="d-flex align-items-center">
                              <h3 class="text-success me-2">${maxImprovement.toFixed(1)}%</h3>
                              <i class="fas fa-arrow-up text-success"></i>
                              <span class="ms-2">em ${categoryNames[mostImprovedCategory]}</span>
                          </div>
                          <p class="text-muted mt-2">
                              Esta categoria apresentou o maior avanço entre as avaliações comparadas.
                          </p>
                      </div>
                  </div>
              </div>`;
          }
      }
      
      resultsHTML += '</div>';
      comparisonResultsDiv.innerHTML = resultsHTML;
  }
  
  // Mostrar a seção de comparação
  document.getElementById('comparison-section').classList.remove('d-none');
}