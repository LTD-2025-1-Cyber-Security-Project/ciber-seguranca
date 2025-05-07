/**
 * Script principal para o DorkOptimizer
 * Sistema de otimização de buscas com Google Dorks
 */

document.addEventListener('DOMContentLoaded', function() {
  // Inicializar todos os tooltips do Bootstrap
  var tooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltips.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Inicializar todos os popovers do Bootstrap
  var popovers = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popovers.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
  });
  
  // Função para mostrar avisos de uso ético
  function showEthicalUseReminder() {
      // Verificar se o aviso já foi mostrado na sessão
      if (!sessionStorage.getItem('ethicalReminderShown')) {
          // Aguardar 3 segundos para mostrar o alerta
          setTimeout(function() {
              // Criar elemento de alerta
              var alertElement = document.createElement('div');
              alertElement.className = 'alert alert-warning alert-dismissible fade show position-fixed bottom-0 end-0 m-3';
              alertElement.setAttribute('role', 'alert');
              alertElement.style.maxWidth = '400px';
              alertElement.style.zIndex = '1050';
              
              alertElement.innerHTML = `
                  <div class="d-flex">
                      <div class="me-3">
                          <i class="fas fa-exclamation-triangle"></i>
                      </div>
                      <div>
                          <h6 class="alert-heading">Lembrete de Uso Ético</h6>
                          <p class="mb-0 small">
                              O DorkOptimizer foi desenvolvido para buscas de informações públicas.
                              Use-o de forma ética e responsável, respeitando privacidade e leis aplicáveis.
                          </p>
                      </div>
                  </div>
                  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
              `;
              
              // Adicionar o alerta ao corpo do documento
              document.body.appendChild(alertElement);
              
              // Marcar como mostrado na sessão
              sessionStorage.setItem('ethicalReminderShown', 'true');
              
              // Configurar para fechar automaticamente após 10 segundos
              setTimeout(function() {
                  var bsAlert = new bootstrap.Alert(alertElement);
                  bsAlert.close();
              }, 10000);
          }, 3000);
      }
  }
  
  // Mostrar o aviso ético apenas em páginas principais
  if (window.location.pathname === '/' || window.location.pathname === '/search') {
      showEthicalUseReminder();
  }
  
  // Detector de inatividade para páginas sensíveis
  if (window.location.pathname === '/search') {
      let inactivityTime = 0;
      const inactivityLimit = 900; // 15 minutos em segundos
      
      // Resetar o contador quando há interação do usuário
      const resetInactivityTimer = function() {
          inactivityTime = 0;
      };
      
      // Eventos que resetam o contador de inatividade
      ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(function(event) {
          document.addEventListener(event, resetInactivityTimer, true);
      });
      
      // Verificar inatividade a cada segundo
      setInterval(function() {
          inactivityTime++;
          
          // Se atingir o limite de inatividade, limpar dados sensíveis
          if (inactivityTime >= inactivityLimit) {
              // Limpar formulários e resultados de busca
              const searchForm = document.getElementById('searchForm');
              const resultCard = document.getElementById('resultCard');
              
              if (searchForm) {
                  searchForm.reset();
              }
              
              if (resultCard && resultCard.style.display !== 'none') {
                  resultCard.style.display = 'none';
                  
                  // Criar alerta de sessão expirada
                  const alertContainer = document.createElement('div');
                  alertContainer.className = 'alert alert-info mt-4';
                  alertContainer.innerHTML = `
                      <i class="fas fa-clock me-2"></i>
                      <strong>Sessão expirada por inatividade.</strong> Os resultados foram limpos por segurança.
                  `;
                  
                  // Adicionar alerta antes do formulário
                  searchForm.parentNode.insertBefore(alertContainer, searchForm);
                  
                  // Remover o alerta após 10 segundos
                  setTimeout(function() {
                      alertContainer.remove();
                  }, 10000);
              }
              
              // Resetar o contador após limpar
              resetInactivityTimer();
          }
      }, 1000);
  }
  
  // Detectar e ajustar para o modo escuro do sistema
  function detectColorScheme() {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
          document.body.classList.add('dark-mode');
      } else {
          document.body.classList.remove('dark-mode');
      }
  }
  
  // Verificar o esquema de cores inicialmente
  detectColorScheme();
  
  // Monitorar mudanças no esquema de cores do sistema
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', detectColorScheme);
});