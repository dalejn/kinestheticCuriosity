function [a,b,c,d,e,sequence] = errwLevyFunction(a,b,c,d,e)
%Levy flight with edge reinforcement
%   a = number of max steps random walker can take
%   b = edge reinforcement value
%   c = levy coefficient (1 < d <= 3)
%   d = max step size (usually set to diameter of underlying graph)
%   e = path to a .mat file with graph object G as underlying graph structure

load(e); % load graph object G from the path f
numberOfSteps = a; % set max number of steps
deltaw = b; % edge reinforcement value

x = 1:1:d; % set upper bound for step size
pdf_levy = double(x) .^ (-c); % set u value, where 1 <= u <= 3
pdf_levy = pdf_levy./sum(pdf_levy);

connectedNodes = G.Edges; % Determine coordinates of connected nodes
startCoord = table2array(datasample(connectedNodes,1)); % Random first step
levy_source_nodes = zeros(1,numberOfSteps);
levy_target_nodes = zeros(1,numberOfSteps);
errwLevy_weights = zeros(1,numberOfSteps);
levy_source_nodes(1,1) = startCoord(1,1); 

for k = 1:numberOfSteps
    step_size = randsample(x,1.,true,pdf_levy); % draw step size from Levy distribution
    source_nodes = zeros(1,step_size);
    target_nodes = zeros(1,step_size);
    
    if k == 1 % first source node
        source_nodes(1,1) = startCoord(1,1);
    else
        source_nodes(1,1) = levy_source_nodes(1,k); 
    end
    
    for step = 1:step_size
        nextNode = neighbors(G,source_nodes(1,step)); % Determine neighboring nodes (no self-loops)
        s = repelem(source_nodes(1,step),length(nextNode));
        adj_mat = findedge(G, s, nextNode);
        transition_prob = G.Edges.Weight(adj_mat);
        if length(transition_prob) == 1 % if there's only 1 connection then move there
            target_nodes(1,step) = nextNode;
            source_nodes(1,step+1) = nextNode;
        else
            target_nodes(1,step) = randsample(nextNode,1,true,transition_prob);
            source_nodes(1,step+1) = target_nodes(1,step);
        end
        if step==step_size % did we reach end of loop
            idxOut = findedge(G,source_nodes(1,step),target_nodes(1,step)); % get edge index
            if idxOut == 0 % if there's no connection, then exit loop
                levy_target_nodes(1,k) = target_nodes(1,step);
                levy_source_nodes(1,k+1) = target_nodes(1,step);
                break
            end
            G.Edges.Weight(idxOut) = G.Edges.Weight(idxOut) + deltaw; % reinforce edge weight
            errwLevy_weights(1,k) = G.Edges.Weight(idxOut); % record weight
            levy_target_nodes(1,k) = target_nodes(1,step);

            if k==numberOfSteps % did we reach the end of the walk?
                break
            else
                levy_source_nodes(1,k+1) = target_nodes(1,step);
            end
        end
    end
end

% Code to plot the path on the underlying network
%%%% Highlight path (red star = start, red x = finish. green dots =
%%%% intermediate nodes. red lines = edges traversed
xy = zeros(k,2);
xy(:,1) = levy_source_nodes(1,1:k);
xy(:,2) = levy_target_nodes(1,1:k);
%xy2 = sort(xy,2);
%uRows = unique(xy2,'rows');
%a = mat2cell(uRows,ones(1,size(uRows,1)),2); % convert to cell for cellfun
%g = @(row)nnz(ismember(xy2,row,'rows')); % function handle that takes a 1x2 row vector as input 
% and returns the number of matching rows in A.
%xy_count = zeros(length(uRows),3);
%xy_count(:,1:2) = uRows;
%xy_count(:,3) = cellfun(g,a); % count of unique edges

% connected_levy_source_nodes = [];
% connected_levy_target_nodes = [];
% disconnected_levy_source_nodes = [];
% disconnected_levy_target_nodes = [];
% 
% for i = 1:k;
%     idxOut = findedge(G,levy_source_nodes(1,i),levy_target_nodes(1,i));
%     if idxOut > 0;
%         connected_levy_source_nodes = [connected_levy_source_nodes levy_source_nodes(1,i)];
%         connected_levy_target_nodes = [connected_levy_target_nodes levy_target_nodes(1,i)];
%     else 
%         disconnected_levy_source_nodes = [disconnected_levy_source_nodes levy_source_nodes(1,i)];
%         disconnected_levy_target_nodes = [disconnected_levy_target_nodes levy_target_nodes(1,i)];
%     end
% end
% 
% h = plot(G,'NodeColor','k','EdgeAlpha',0.5,'EdgeColor',[0.8 0.8 0.8]);
% %%%% highlight the disconnected nodes
% highlight(h,disconnected_levy_source_nodes,'NodeColor','y','Marker','*');
% highlight(h,disconnected_levy_target_nodes,'NodeColor','y','Marker','*');
% %%%% set weight determined by duplicate edges
% highlight(h,connected_levy_source_nodes,connected_levy_target_nodes,'EdgeColor','b','NodeColor','c','Marker','*');
% %%%% label the first point
% start_pt = levy_source_nodes(1,1);
% highlight(h,levy_source_nodes(1,1),'NodeColor','r','Marker','*','MarkerSize',7);
% %%%% label the last point
% highlight(h,levy_target_nodes(1,k),'NodeColor','r','Marker','x','MarkerSize',7);
% title('Edge-Reinforced Levy Flight', 'FontSize', 20);
% G.Edges.LWidths = 7*G.Edges.Weight/max(G.Edges.Weight);
% h.LineWidth = G.Edges.LWidths;

% errwLevy_xy = xy;
% 
% unique_nodes = unique(errwLevy_xy); % retrieve unique nodes walked over
% errwLevy_subgraph = subgraph(G, unique_nodes); % extract subgraph
% 
% h = plot(errwLevy_subgraph);
% errwLevy_subgraph.Edges.LWidths = 7*errwLevy_subgraph.Edges.Weight/max(errwLevy_subgraph.Edges.Weight);
% h.LineWidth = errwLevy_subgraph.Edges.LWidths;
% labelnode(h,[1:length(unique_nodes)],{''});

sequence = zeros(k+1,1);
sequence(1,1) = xy(1,1);
sequence(2:k+1,1) = xy(:,2);

end

